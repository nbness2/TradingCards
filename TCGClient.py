import socket, sys
from msvcrt import getwch, putwch, putch


def client(shost, sport):
    # Talk to server until disconnected.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((shost, sport))
        while True:
            reply = s.recv(256).decode()[:256]
            if len(reply) == 0:
                reply = '9'
            command = int(reply[0])
            data = reply[1:]
            if command == 0x00:
                print(data)
                s.send('1'.encode())
            elif command == 0x01:
                valid = False
                while not valid:
                    message = input(data)
                    if len(message):
                        valid = True
                s.send(message[:32].encode())
            elif command == 0x02:
                valid = False
                while not valid:
                    message = getchstr()
                    if len(message):
                        valid = True
                s.send(message[:32].encode())
            elif command == 0x09:
                break
        s.close()

    except:
        s.close()
    sys.exit()

def getchstr():
    string = ''
    while True:
        char = chr(ord(getwch()))
        if char in ('\r', '\n', '\b', '\x08'):
            if char in ('\b', '\x08'):
                if len(string):
                    string = string[:-1]
                    putwch('\b')
            else:
                putwch('\n')
                return string
        else:
            string += char
        putwch(' ')
        clrline()
        putstr('*'*len(string))


def putstr(string):
    for char in string:
        putch(char.encode())

def clrline():
    putstr('\b'*80)

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 1337
    while True:
        client(host, port)
