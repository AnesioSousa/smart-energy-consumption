#!/usr/bin/env python3

import socket


# self.send_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_TYPE)


def writeFile(client):
    namefile = str(input('Name file>'))
    try:
        client.send(namefile.encode('utf-8'))
        # Melhorar essa exception!
    except:
        return print("some error occurred")


def openfile(client, namefile, mode):
    with open(namefile, mode) as file:
        while True:
            data = client.recv(10_000)
            if not data:
                break
            file = file.write(data)
            print(f'{namefile} received !')


def sendMessages(client, username):
    while True:
        try:
            msg = input('\n')
            client.send(f'<{username}> {msg}'.encode('utf-8'))
        except:
            return print("Houve um erro")


def main():
    HOST = 'localhost'
    PORT = 65136

    send_to_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        send_to_server.connect((HOST, PORT))
    except:
        return print('\nNão foi possívvel se conectar ao servidor!\n')

    username = input('Usuário> ')
    print('\nConectado')

    sendMessages(send_to_server, username)


main()
