#!/usr/bin/env python3

import threading
import socket


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


def dataTreatment(client):
    while True:
        try:
            future = recvall(client, 225)
            print(future)
        except Exception as e:
            print(e.args[0])


# Quando coloco o @classmethod não vai...
# Sobrecarregar esse método para receber o socket


def UDPstart_listening(host, port):
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Pra não deixar processos conectados. Quando o processo morrer fecha tudo
    # UDPServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Até aqui")
    try:
        UDPServerSocket.bind((host, port))
        UDPServerSocket.listen()

        print(f'Server is running on: {UDPServerSocket.getsockname()}')
    except Exception as exc:
        print('exception: %s' % exc)

    print("Um monitor conectou")
