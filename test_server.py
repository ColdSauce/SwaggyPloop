#!/usr/bin/python

import socket

def resolve(name):
    return "penis"

host = ''
port = 53
backlog = 5
size = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host,port))
s.listen(backlog)
print('ready')
while 1:
    client, address = s.accept()
    data = client.recv(size)
    print(client, address)
    print(data)
    if data:
        bits = data.split(":")
        if bits[0] == 'h':
            client.send(resolve(bits[1]))
    client.close()
