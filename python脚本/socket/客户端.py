# coding=UTF-8
import socket,sys

HOST = '127.0.0.1'
PORT = 6666
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    s.connect((HOST,PORT))
except Exception as e:
    print('Server no found!')
    sys.exit()
while True:
    c = input('YOU SAY:')
    s.sendall(c.encode())
    data = s.recv(1024)
    data = data.decode()
    print('Received :',data)
    if c.lower()=='再见':
        break