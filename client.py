#!/usr/bin/env python3

import socket


HOST = "127.0.0.1"
PORT = 65432

request_text = """\
GET /apostador HTTP/1.1\r\n\
Host: 127.0.0.1\r\n\
User-Agent: search1.py \r\n\
Connection: close\r\n\
\r\n\
"""
# se esse arquivo for executado como main
if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    sock.sendall(request_text.encode('ascii'))
    raw_reply = b''
    while True:
        more = sock.recv(1024)
        if not more:
            break
        raw_reply += more
        print(raw_reply.decode('utf-8')+'\n')
