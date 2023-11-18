import socket

host = ('185.189.102.64', 6112)
sock = socket.create_connection(host)
print(sock.recv(1024))
while True:
    sock.sendall(b'\FF')