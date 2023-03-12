#!/usr/bin/env python3
import socket
import threading
import multiprocessing


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
    pass


def main():
    HOST = 'localhost'
    UDPPORT = 65120
    MAX_BYTES = 65535

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        UDPServerSocket.bind((HOST, UDPPORT))
        print(f'Server is running on: {UDPServerSocket.getsockname()}')
    except Exception as exc:
        print('exception: %s' % exc)

    while True:
        data, address = UDPServerSocket.recvfrom(MAX_BYTES)
        text = data.decode('ascii')
        print('The client at {} says {!r}'.format(address, text))
        text = 'Your data was {} bytes long'.format(len(data))
        data = text.encode('ascii')
        UDPServerSocket.sendto(data, address)


main()
