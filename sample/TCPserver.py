#!/usr/bin/env python3

import threading
import socket
import concurrent.futures
import sys
import json

from time import sleep
from multiprocessing import Process
from UDPserver import *

# O que vai rodar no processo principal? Já que to usando thread pra tudo?


def broadcast(msg, client):
    """for clientItem in clients:
        if clientItem != client:
            try:
                clientItem.send(msg)
            except:
                deleteClient(clientItem)"""
    pass


def deleteClient(client):
    # clients.remove(client)
    pass


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
    while True:
        try:
            future = recvall(client, 225)
            print(parse_message(future))
            # broadcast(msg, client)
        except:
            deleteClient(client)
            break

# Quando coloco o @classmethod não vai...
# Sobrecarregar esse método para receber o socket


def start_listening(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Pra não deixar processos conectados. Quando o processo morrer fecha tudo
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((host, port))
        server.listen()

        print(f'Server is running on: {server.getsockname()}')
    except Exception as exc:
        print('exception: %s' % exc)
        return print('\nNão foi possível iniciar o servidor!\n')

    while True:
        client, addr = server.accept()
        socket_type = client.getsockopt(socket.SOL_SOCKET, socket.SO_TYPE)

        match socket_type:
            case socket.SOCK_DGRAM:
                print("Um monitor conectou")
                # Ou eu crio uma nova thread ou passo pro processo fazê-lo
                # client.close()
            case socket.SOCK_STREAM:
                # Ou eu crio uma nova thread ou passo pro processo fazê-lo
                print("Um cliente conectou!\n")

                print('end of message')
                thread = threading.Thread(
                    target=messagesTreatment, args=[client])
                thread.start()
                client.close()

                """
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future = executor.submit(recvall, client, 16)
                print(future)

                """
            case _:
                print("Requisição inválida!")


if __name__ == "__main__":
    HOST = 'localhost'
    TCPPORT = 65136
    UDPPORT = 65120

    p = Process(target=UDPstart_listening, args=(HOST, UDPPORT))
    p.start()
    p.join()

    thread = threading.Thread(target=start_listening, args=(HOST, TCPPORT))
    thread.start()
