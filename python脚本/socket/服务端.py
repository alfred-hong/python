# coding=UTF-8
import socket

language = {'what is your name': 'my name is tom',
            'how old are you': '25', 'bye': 'bye'}
HOST = '127.0.0.1'
PORT = 6666
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(1)
print("Listing at port 6666")
conn,addr = s.accept()
print('Connect by:',addr)
while True:
    data = conn.recv(1024)
    data = data.decode()
    if not data:
        break
    print('Received message:',data)
    conn.sendall(language.get(data,'Nothing').encode())
conn.close()
s.close()