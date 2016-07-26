import sys, time, socketserver
import emailinfo, regrules, TCGMain
from modules import pyrand, pyemail, pyhash
from queues import Queue
from threading import Thread
from os import walk, makedirs


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, request_handler):
        socketserver.TCPServer.__init__(self, server_address, request_handler)


class UserHandler(socketserver.BaseRequestHandler):
    message = {
             'register_username': 'Min 4 characters, max 16 characters.\nEnter desired username: ',
             'register_password': '\nMin 8 characters, max 32 characters. Must have at least 1 letter and number.\nCannot contain symbols.\nEnter password: ',
             'register_email': '\nYour activation code will be sent to this email.\nEnter a valid email: ',
             'activate_username': 'Enter the username of the account you wish to activate: ',
             'activate_password': 'Enter the password of the account you wish to activate: ',
             'activate_email': 'Enter the email you used to register this account: ',
             'activation_code': 'Enter the activation code found in your email: ',
             'act_success': 'Your account has been successfully activated.',
             'invalid_act_code': 'Invalid Username, Password or Activation Code',
             'not_activated': 'This account has not been activated yet.',
             'already_activated': 'That account has already been activated. ',
             'registration_success': 'Your account has been registered and an activation code has been sent to your email.',
             'login_success': 'Successfully logged in.',
             'invalid_up': 'Invalid Username or Password.',
             'login_activate_register': '(L)ogin, (A)ctivate, or (R)egister: '
             }

    def handle(self):
        while True:
            response = send_receive(self.request, self.message['login_activate_register']).lower()
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
        passhash = pyhash.Sha384(send_receive(socket, 'Password: ', recvsize=32)).hexdigest()
        activated, activation_code, user_passhash, user_emailhash = read_user(username)
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
            username = send_receive(socket, self.message['activate_username'], recvsize=16)
            passhash = pyhash.Sha384(send_receive(socket, self.message['activate_password'], recvsize=32)).hexdigest()
        user_activated, user_activation_code, user_passhash, user_emailhash = read_user(username)
        user_activated = int(user_activated)
        del user_emailhash
        if user_activated:
            send_receive(socket, self.message['already_activated'], 'p')
        else:
            activation_code = send_receive(socket, self.message['activation_code'], recvsize=11)
            if passhash == user_passhash and activation_code == user_activation_code:
                queues['activation'][0].put(username)
                send_receive(socket, self.message['act_success'], 'p')
            else:
                send_receive(socket, self.message['invalid_act_code'], 'p')

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
                username = send_receive(socket, self.message['register_username'], recvsize=16)
                password = send_receive(socket, self.message['register_password'], recvsize=32)
                useremail = send_receive(socket, self.message['register_email'], recvsize=64)
                paramchecks = check_details(username, password, useremail)
                passhash = pyhash.Sha384(password).hexdigest()
                del password
                if type(paramchecks) == bool:
                    passed = True
            del paramchecks, passed
            ehash = pyhash.Sha384(useremail.lower()).hexdigest()
            activation_code = pyhash.Md5(pyrand.randstring(16)).hexdigest[::3]
            queues['register'][0].put((username, (0, activation_code, passhash, ehash)))
            emessage = 'Dear {0}, Thank you for registering your account with pyTCG! Your activation code is:\n{1}\n'.format(username, activation_code)
            email_params = (useremail, emessage, 'pyTCG activation code', email, emailpass, smtpaddr, False)
            queues['email'][0].put(email_params)
            del username, activation_code, passhash, ehash,
            send_receive(socket, self.message['registration_success'], 'p', 1)
        except Exception as e:
            write_error(e) #not good practise but if problems do happen i can add exceptions for those cases

    def menu(self): #cli menu
        pass


class LoginContainer(Thread, dict):
    def __init__(self):
        dict.__init__(self)
        Thread.__init__(self)

    def add_sess(self, sessname):
        self[sessname] = pyhash.Md5(sessname+pyrand.randstring(2))[:16]

    def del_sess(self, sessname):
        del self[sessname]


class Session:
    def __init__(self, socket):
        self.socket = socket


class QueueWorker(Thread):
    def __init__(self, params):
        Thread.__init__(self)
        self.queue, self.funct = params

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
    commands = {'p': 0x00, 'i': 0x01, 'q': 0x09}
    send_data = str(commands[stype])+sendmsg
    socket.send(send_data.encode())
    if stype == 'i':
        recv_data = socket.recv(64).decode()[:recvsize]
        return recv_data
    socket.recv(64)[:1]


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

    if password:
        passwordc = regrules.check_password(password)
        del password
        if len(passwordc):
            faults['Password'].extend(passwordc)

    if username:
        usernamec = regrules.check_username(username)
        if len(regrules.check_username(username)):
            faults['Username'].extend(usernamec)

    if username.lower() in read_usernames():
        faults['Username'].append('username taken')

    if email:
        emailc = regrules.check_email(email)
        del email
        if type(emailc) != bool:
            faults['Email'].append(emailc)

    for fault in faults:
        if len(fault):
            return faults
    return True


def read_usernames(userdir='users'):
    return [username[:-4] for username in walk(userdir).__next__()[2]]


def write_user(details, userdir='users/'):
    makedir('users/')
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


def write_error(exception):
    with open('errors.txt', 'w') as errfile:
        errfile.write(str(exception))


def makedir(path):
    makedirs(path, exist_ok=True)

incloginlimit = 5
inclogintimeout = 600

email, emailpass, smtpaddr = emailinfo.info

HOST = ''
PORT = 1337

queues = {
    'register': [Queue('l'), write_user],
    'activation': [Queue('l'), activate_user],
    'email': [Queue('l'), pyemail.send_email],
    }

meow = True

workers = {queue: QueueWorker(queues[queue]) for queue in queues}

if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), UserHandler)
    try:
        for queue in queues:
            workers[queue].start()
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(e)
        sys.exit(0)
