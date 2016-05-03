import sys, time, socketserver
import emailinfo, regrules, TCGMain
from modules import pyrand, pyemail, pyhash
from queue import Queue
from threading import Thread
from os import walk


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, request_handler):
        socketserver.TCPServer.__init__(self, server_address, request_handler)


class UserHandler(socketserver.BaseRequestHandler):
    message = {
             'regusername': 'Min 4 characters, max 16 characters.\nEnter desired username: ',
             'regpassword': '\nMin 8 characters, max 32 characters. Must have at least 1 letter and number.\nCannot symbols.\nEnter password: ',
             'regemail': '\nYour activation code will be sent to this email.\nEnter a valid email: ',
             'actusername': 'Enter the username of the account you wish to activate: ',
             'actpassword': 'Enter the password of the account you wish to activate: ',
             'actemail': 'Enter the email you used to register this account: ',
             'actcode': 'Enter the activation code found in your email: ',
             'act_success': 'Your account has been successfully activated.',
             'invalid_act': 'Invalid Username, Password or Activation Code',
             'not_activated': 'This account has not been activated yet.',
             'alreadyact': 'That account has already been activated. ',
             'registered': 'Your account has been registered and an activation code has been sent to your email.',
             'login_success': 'Successfully logged in.',
             'invalid_up': 'Invalid Username or Password.',
             'log/act/reg': '(L)ogin, (A)ctivate, or (R)egister: '
             }

    def handle(self):
        while True:
            response = send_receive(self.request, self.message['log/act/reg']).lower()
            if response == 'l':
                self.login()
            elif response == 'a':
                self.activate()
            elif response == 'r':
                self.register()
            elif response == '~':
                break
            else:
                send_receive(self.request, 'Invalid choice: '+response, 'p')
        send_receive(self.request, 'Thank you for choosing pyTCG!', 'p')
        self.request.close()

    def login(self):
        socket = self.request
        username = send_receive(socket, 'Username: ', recvsize=16)
        passhash = pyhash.Sha384(send_receive(socket, 'Password: ', recvsize=32)).hexdigest
        activated, actcode, user_passhash, user_emailhash = read_user(username)
        activated = int(activated)
        if passhash == user_passhash:
            if activated:
                send_receive(socket, self.message['login_success'], 'p')
            else:
                send_receive(socket, self.message['not_activated'], 'p')
                self.activate(username, passhash)
        else:
            send_receive(socket, self.message['invalid_up'], 'p')

    def activate(self, username=None, passhash=None):
        socket = self.request
        if not (username and passhash):
            username = send_receive(socket, self.message['actusername'], recvsize=16)
            passhash = pyhash.Sha384(send_receive(socket, self.message['actpassword'], recvsize=32)).hexdigest
        user_activated, user_actcode, user_passhash, user_emailhash = read_user(username)
        user_activated = int(user_activated)
        del user_emailhash
        if user_activated:
            send_receive(socket, self.message['alreadyact'], 'p')
        else:
            activation_code = send_receive(socket, self.message['actcode'], recvsize=8)
            if passhash == user_passhash and activation_code == user_actcode:
                queues['activation'].put(username)
                send_receive(socket, self.message['act_success'], 'p')
            else:
                send_receive(socket, self.message['invalid_act'], 'p')

    def register(self):
        try:
            socket = self.request
            passed = False
            useremail, password, username = ('', '', '')
            paramchecks = {}
            while not passed:
                if len(paramchecks):
                    estring = err_str(paramchecks, ['Username', 'Password', 'Email'])
                    send_receive(socket, estring, 'p', 1)
                    del estring
                username = send_receive(socket, self.message['regusername'], recvsize=16)
                password = send_receive(socket, self.message['regpassword'], recvsize=32)
                useremail = send_receive(socket, self.message['regemail'], recvsize=64)
                paramchecks = check_details(username, password, useremail)
                passhash = pyhash.Sha384(password).hexdigest
                del password
                if type(paramchecks) == bool:
                    passed = True
            del paramchecks, passed
            ehash = pyhash.Sha384(useremail.lower()).hexdigest
            activation_code = pyhash.Md5(pyrand.randstring(16)).hexdigest[::4]
            queues['register'].put((username, (0, activation_code, passhash, ehash)))
            emessage = 'Dear {0}, Thank you for registering your account with pyTCG! Your activation code is:\n{1}\n'.format(username, activation_code)
            email_params = (useremail, emessage, 'pyTCG activation code', email, emailpass, smtpaddr, False)
            queues['email'].put(email_params)
            del username, activation_code, passhash, ehash,
            send_receive(socket, self.message['registered'], 'p', 1)
        except Exception as e:
            print(e)


class LoginContainer(Thread):
    def __init__(self):
        Thread.__init__(self)

    def add_sess(self, sessname):
        self[sessname] = pyhash.Md5(sessname+pyrand.randstring(2))[:16]

    def del_sess(self, sessname):
        del self[sessname]


class Session:
    def __init__(self, socket):
        self.socket = socket


class QueueWorker(Thread):
    def __init__(self, queue, funct):
        Thread.__init__(self)
        self.queue = queue
        self.funct = funct

    def run(self):
        while True:
            try:
                if not self.queue.empty():
                    parts = self.queue.get()
                    self.funct(parts)
            except:
                self.queue.put(parts)


def send_receive(socket, sendmsg, stype='i', recvsize=1):
    # Sends encoded data + command, returns decoded receive data
    # p, 0x00 = no input
    # i, 0x01 = input
    commands = {'p': 0x00, 'i': 0x01}
    sendData = str(commands[stype])+sendmsg
    socket.send(sendData.encode())
    if stype == 'i':
        recvData = socket.recv(recvsize).decode()[:recvsize]
        return recvData
    socket.recv(recvsize)[:1]


def err_str(errdict, paramorder=()):
    estring = ''
    for param in paramorder if len(paramorder) else errdict.keys():
        if len(errdict[param]):
            estring += '\n'+param+': '
        for error in errdict[param]:
            estring += error+', '
    return estring[:-2]+'\n'


def check_details(username=None, password=None, email=None):
    faults = {'Username': [], 'Password': [], 'Email': []}
    full_pass = True

    if password:
        passwordc = regrules.check_password(password)
        del password
        if len(passwordc):
            full_pass = False
            faults['Password'].extend(passwordc)

    if username:
        usernamec = regrules.check_username(username)
        if len(usernamec):
            full_pass = False
            faults['Username'].extend(usernamec)

    if username.lower() in read_usernames():
        full_pass = False
        faults['Username'].append('username taken')

    if email:
        emailc = regrules.check_email(email)
        del email
        if type(emailc) != bool:
            full_pass = False
            faults['Email'].append(emailc)

    if full_pass:
        return True
    return faults


def read_usernames(userdir='users'):
    return [username[:-4] for username in walk(userdir).__next__()[2]]


def write_user(details, userdir='users/'):
    username, details = details
    username += '.usr'
    with open(userdir+username.lower(), 'w') as ufile:
        for detail in details:
            ufile.write(str(detail)+'\n')
    return True


def read_user(username, userdir='users/'):
    username += '.usr'
    with open(userdir+username.lower(), 'r') as ufile:
        details = tuple([detail.strip() for detail in ufile.readlines()])
    #user['activated'], user['actcode'], user['passhash'], user['emailhash'] = details
    return details


def is_activated(username, userdir='users/'):
    if read_user(username, userdir)[0]:
        return True
    return False


def activate_user(username, userdir='users/'):
    user_details = list(read_user(username, userdir))
    user_details[0] = 1
    write_user((username, user_details), userdir)
    return True

#loginQueue = Queue()

#this is the time you cannot log in after so many attempts
incloginlimit = 5
inclogintimeout = 600

email, emailpass, smtpaddr = emailinfo.info

HOST = ''
PORT = 1337

queues = {
    'register': Queue(),
    'activation': Queue(),
    'email': Queue(),
    }

workers = {
    'register': QueueWorker(queues['register'], write_user),
    'activation': QueueWorker(queues['activation'], activate_user),
    'email': QueueWorker(queues['email'], pyemail.send_email)
    }

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), UserHandler)
    try:
        for queue in queues:
            workers[queue].start()
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
