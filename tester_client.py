import socket

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.connect(('localhost', 8089))
msg = 'hello'
clientsocket.send(msg.encode())

while True:
    buf = clientsocket.recv(64)
    buf = buf.decode('utf-8')
    if len(buf) > 0:
        print(buf)
        break

        # import sys
        #
        # sys.path.insert(0, '/Users/ruthbrennan/Documents/5th_Year/cs7ns1-meshd/')  # location of src
