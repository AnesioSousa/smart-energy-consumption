#!/usr/bin/env python3

import socket


HOST = "127.0.0.1"
PORT = 65432


def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    sc, sockname = sock.accept()
    with sc:
        print(f'We have accepted a connection from {sockname}')
        while True:
            message = sc.recv(1024)
            if not message:
                break
            sc.sendall(message)
