import socketserver, sys, regrules
from modules import pyrand, pyemail, pyhash
import emailinfo

email = emailinfo.email
emailpass = emailinfo.password
smtpaddr = emailinfo.smtp

HOST = ''
PORT = 1337

class UserHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.register()
        self.request.close

    def register(self):
        socket = self.request
        allValid = False
        uemail, upass, uname = ('','','')
        paramchecks = {}
        while not allValid:
            if len(paramchecks):
                estring = errstr(paramchecks, ['Username', 'Password', 'Email'])
                sendRecv(socket, estring, 'p', 1)
            uname = sendRecv(socket, 'Min 4 characters, max 16 characters.\nEnter desired username: ', recvsize = 16)
            upass = sendRecv(socket, '\nMin 8 characters, max 32 characters. Must have at least 1 letter and number.\nCannot symbols.\nEnter password: ', recvsize = 32)
            uemail = sendRecv(socket, '\nYour activation code will be sent to this email.\nEnter a valid email: ', recvsize= 64)
            paramchecks = checkupe(uname, upass, uemail)
            if type(paramchecks) == bool:
                allValid = True
        actCode = pyhash.Md5(pyrand.randstring(8)).hexdigest[:8]
        emessage = 'Dear {0}, Thank you for registering your account with pyTCG! Your activation code is:\n{1}'.format(uname, actCode)
        pyemail.sendEmail(uemail, emessage, 'pyTCG activation code',
                          email, emailpass, 'smtp.gmail.com')
        print('email sent to', uemail)


class TestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.close

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)


def sendRecv(socket, sendmsg, stype = 'i', recvsize = 64):
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


def errstr(errdict, paramorder = ()):
    estring = ''
    for param in paramorder if len(paramorder) else errdict.keys():
        if len(errdict[param]):
            estring += '\n'+param+': '
        for error in errdict[param]:
            estring += error+', '
        estring = estring[:-2]
    return estring+'\n'


def checkupe(username, password, email):
    faults = {'Username' : [], 'Password' : [], 'Email' : []}
    fullPass = True

    unamec = regrules.checkUsername(username)
    if len(unamec):
        fullPass = False
        faults['Username'].extend(unamec)

    pwordc = regrules.checkPassword(password)
    if len(pwordc):
        fullPass = False
        faults['Password'].extend(pwordc)

    emailc = regrules.checkEmail(email)
    if type(emailc) != bool:
        fullPass = False
        faults['Email'].append(emailc)

    if fullPass:
        return True
    return faults

if __name__ == "__main__":
    echo = SimpleServer((HOST, PORT), UserHandler)
    try:
        echo.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
