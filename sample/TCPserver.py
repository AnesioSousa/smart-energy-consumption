#!/usr/bin/env python3

import threading
import socket
import concurrent.futures
import multiprocessing
import sys
import json
import asyncio
import signal

# O que vai rodar no processo principal? Já que to usando thread pra tudo?

child_processes = []


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


def parse_message(message):
    # ascii ou utf-8 encoded?
    # qts cabeçalhos?
    # qual o tamanho das mensagens?
    message = message.decode('ascii')
    message = message.split('\r\n')

    req_line = message[0]
    req_line = req_line.split()

    method = req_line[0]
    url = req_line[1]

    content = message[len(message)-1]
    content = json.loads(content)

    return content


def messagesTreatment(client):
    try:
        message = client.recv(2048)
        print(parse_message(message))
    except Exception as exc:
        print('exception: %s' % exc)


def handle_connection(client, address):
    messagesTreatment(client)
    client.close()


def close_child_processes(signum, frame):
    for p in child_processes:
        p.terminate()


def main():
    HOST = 'localhost'
    TCPPORT = 65136

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Pra não deixar conexão. Quando o processo morrer fecha tudo
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, TCPPORT))
        server.listen()
        print(f'Server is running on: {server.getsockname()}')
    except Exception as exc:
        print('exception: %s' % exc)
        return print('\nNão foi possível iniciar o servidor!\nException: %s' % exc)

    signal.signal(signal.SIGTERM, close_child_processes)
    while True:
        client, address = server.accept()

        print("Um cliente conectou!\n")
        proc = multiprocessing.Process(
            target=handle_connection, args=[client, address])
        child_processes.append(proc)
        proc.start()
        print(multiprocessing.active_children())


main()
