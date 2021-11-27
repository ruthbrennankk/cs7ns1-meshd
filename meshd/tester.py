import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 8089))
serversocket.listen(5) # become a server socket, maximum 5 connections

while True:
    connection, address = serversocket.accept()
    buf = connection.recv(64)
    buf = buf.decode('utf-8')
    if len(buf) > 0:
        print(buf)
    msg = 'hello back'
    connection.send(msg.encode())
    break