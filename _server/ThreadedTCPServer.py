import socketserver, sys
import rules, pyemail, pyhash, pyrand


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
        while not allValid:
            uname = sendRecv(socket, '\nMin 4 characters, max 16 characters.\nEnter desired username: ', recvsize = 16)
            upass = sendRecv(socket, '\nMin 8 characters, max 32 characters. Must have at least 1 letter and number.\nCannot symbols.\nEnter password: ', recvsize = 32)
            uemail = sendRecv(socket, '\nYour activation code will be sent to this email.\nEnter a valid email: ', recvsize= 64)
            if False not in checkupe(uname, upass, uemail):
                allValid = True
        actCode = pyhash.Md5(pyrand.randstring(8)).hexdigest()[:8]
        emessage = 'Dear {0}, Thank you for registering your account with pyTCG! Your activation code is:\n{1}'.format(uname, actCode)
        pyemail.sendEmail(uemail, emessage, 'pyTCG activation code',
                          '', '', 'smtp.email.com')
        print('email sent')



class TestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.request.close

class SimpleServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)

def sendRecv(socket, sendmsg, type = 'i', recvsize = 64):
    # Sends encoded data + command, returns decoded receive data
    # p, 0x00 = no input
    # i, 0x01 = input
    commands = {'p' : 0x00, 'i' : 0x01}
    sendData = str(commands[type])+sendmsg
    socket.send(sendData.encode())
    if type == 'i':
        recvData = socket.recv(recvsize).decode()[:recvsize]
        return recvData
    socket.recv(recvsize)[:1]

def checkupe(username, password, email):
    return (rules.checkUsername(username), rules.checkEmail(email), rules.checkPassword(password))

if __name__ == "__main__":
    echo = SimpleServer((HOST, PORT), UserHandler)
    try:
        echo.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)
