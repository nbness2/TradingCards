import socket


def client(host, port):
    # Talk to server until disconnected.
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
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
            elif command == 0x09:
                break
        s.close()

    except:
        s.close()

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 1337
    while True:
        client(host, port)
