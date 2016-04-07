import socketserver, sys, regrules
import emailinfo
from modules import pyrand, pyemail, pyhash
from queue import Queue
from threading import Thread
from os import walk


class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


class UserHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            self.register()
            self.request.close()
        except:
            pass

    def login(self):
        socket = self.request
        username = send_receive(socket, 'Username: ', recvsize = 16)
        passhash = pyhash.Md5(send_receive(socket, 'Password: ', recvsize = 32)).hexdigest
        activated = is_activated(username)
        while not activated:
            self.activate()


    def activate(self):
        socket = self.request
        pass


    def register(self):
        socket = self.request
        allValid = False
        useremail, password, username = ('', '', '')
        paramchecks = {}
        while not allValid:
            if len(paramchecks):
                estring = err_str(paramchecks, ['Username', 'Password', 'Email'])
                send_receive(socket, estring, 'p', 1)
            username = send_receive(socket, 'Min 4 characters, max 16 characters.\nEnter desired username: ', recvsize = 16)
            password = send_receive(socket, '\nMin 8 characters, max 32 characters. Must have at least 1 letter and number.\nCannot symbols.\nEnter password: ', recvsize = 32)
            useremail = send_receive(socket, '\nYour activation code will be sent to this email.\nEnter a valid email: ', recvsize = 64)
            paramchecks = check_all(username, password, useremail)
            if type(paramchecks) == bool:
                allValid = True
        passhash = pyhash.Sha384(password).hexdigest
        del password, paramchecks, allValid
        ehash = pyhash.Sha384(useremail.lower()).hexdigest
        activation_code = pyhash.Md5(pyrand.randstring(16)).hexdigest[::4]
        regQueue.put(write_user(username, (False, activation_code, passhash, ehash)))
        emessage = 'Dear {0}, Thank you for registering your account with pyTCG! Your activation code is:\n{1}'.format(username, activation_code)
        del username, activation_code
        send_receive(socket, 'Your account has been registered, and an activation code has been sent to your email.', 'p', 0)


class TestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.close






    # Sends encoded data + command, returns decoded receive data
    # p, 0x00 = no input
    # i, 0x01 = input
    commands = {'p' : 0x00, 'i' : 0x01}
    sendData = str(commands[stype])+sendmsg
    socket.send(sendData.encode())
    if stype == 'i':
        recvData = socket.recv(recvsize).decode()[:recvsize]
        return recvData
    socket.recv(recvsize)[:1]


def err_str(errdict, paramorder = ()):
    estring = ''
    for param in paramorder if len(paramorder) else errdict.keys():
        if len(errdict[param]):
            estring += '\n'+param+': '
        for error in errdict[param]:
            estring += error+', '
        estring = estring[:-2]
    return estring+'\n'


def check_all(username, password, email):
    faults = {'Username' : [], 'Password' : [], 'Email' : []}
    fullPass = True

    usernamec = regrules.check_username(username)
    if len(usernamec):
        fullPass = False
        faults['Username'].extend(usernamec)

    passwordc = regrules.check_password(password)
    if len(passwordc):
        fullPass = False
        faults['Password'].extend(passwordc)

    emailc = regrules.check_email(email)
    if type(emailc) != bool:
        fullPass = False
        faults['Email'].append(emailc)

    if fullPass:
        return True
    return faults


def read_usernames(dirname = 'users'):
    return [username[:-4] for username in walk(dirname).__next__()[2]]

def writeuser(details, userdir = 'users/'):
    uname = details[0]+'.usr'
    details = details[1:]
    with open(userdir+uname, 'w') as ufile:
        for detail in details:
            detail = str(detail)+'\n'
            ufile.write(detail)
    return True


def read_user(username, userdir = 'users/'):
    username += '.usr'
    #user = {'activated':None, 'actcode':None, 'passhash':None, 'emailhash':None}
    with open(userdir+username, 'r') as ufile:
        details = tuple([detail.strip() for detail in ufile.readlines()])
    #user['activated'], user['actcode'], user['passhash'], user['emailhash'] = details
    return details

def queueworker(queue):
    while True:
        try:
            if not queue.empty():
                queue.get()
        except:
            pass

regQueue = Queue()
loginQueue = Queue()
#sessions = {'username':'sessionid'}

email = emailinfo.email
emailpass = emailinfo.password
smtpaddr = emailinfo.smtp

HOST = ''
PORT = 1337


if __name__ == "__main__":
    server = SimpleServer((HOST, PORT), UserHandler)
    try:
        regqworker = QueueWorker(regQueue)
        #logqworker = QueueWorker(loginQueue)
        regqworker.start()
        #logqworker.start()
        server.serve_forever()
        queueworker(regQueue)
    except KeyboardInterrupt:
        sys.exit(0)
