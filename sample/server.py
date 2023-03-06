#!/usr/bin/env python3

import threading
import socket


class Server(threading.Thread):
    clients = []

    def __init__(self, host, port):
        self.__host = host
        self.__port = port

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, value):
        self.__host = value

    @property
    def port(self):
        return self.__port

    @port.setter
    def port(self, value):
        self.__port = value

    @classmethod
    def recvall(self, sock, length):
        data = b''

        while len(data) < length:
            more = sock.recv(length - len(data))
            if not more:
                raise EOFError('was expecting %d bytes but only received'
                               ' %d bytes before the socket closed'
                               % (length, len(data)))
            data += more

        return data

    @classmethod
    def messagesTreatment(self, client):
        while True:
            try:
                msg = client.recv(2048)
                self.broadcast(msg, client)
            except:
                self.deleteClient(client)
                break

    # Quando coloco o @classmethod não vai...
    # Sobrecarregar esse método para receber o socket
    def start_listening(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((self.host, self.port))
            server.listen()
            print(f'Server is running on: {server.getsockname()}')
        except:
            return print('\nNão foi possível iniciar o servidor!\n')

        while True:
            client, addr = server.accept()
            self.clients.append(client)

            print('We have accepted a connection from', addr)
            print(' Socket name:', client.getsockname())
            print(' Socket peer:', client.getpeername())

            message = self.recvall(client, 16)
            print(' Incoming sixteen-octet message:', repr(message))
            client.sendall(b'Farewell, client')
            client.close()
            print(' Reply sent, socket closed')

            thread = threading.Thread(
                target=self.messagesTreatment, args=[client])
            thread.start()

    @classmethod
    def broadcast(self, msg, client):
        for clientItem in self.clients:
            if clientItem != client:
                try:
                    clientItem.send(msg)
                except:
                    self.deleteClient(clientItem)

    @classmethod
    def deleteClient(self, client):
        self.clients.remove(client)
