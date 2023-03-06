#!/usr/bin/env python3

import socket
import threading


class Sensor():
    def __init__(self, host, port):
        print("entrou")
        self.__host = host
        self.__port = port
        # serial number = bcrypt
        self.send_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connect()
        self.openfile('teste.txt', 'w')
        self.writeFile()

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
    def receiveMessages(self):
        while True:
            try:
                msg = self.send_to_server.recv(2048).decode('utf-8')
                print(msg+'\n')
            except:
                print('\nNão foi possível permanecer conectado ao servidor!\n')
                print('Pressione <Enter> Para continuar...')
                self.send_to_server.close()
                break

    @classmethod
    async def connect(self):
        try:
            await self.send_to_server.connect(self.host, self.port)
        except:
            print('\nNão foi possível se conectar ao servidor')

    @classmethod
    def writeFile(self):
        namefile = str(input('Name file>'))
        try:
            self.send_to_server.send(namefile.encode('utf-8'))
            # Melhorar essa exception!
        except:
            return print("some error occurred")

    def openfile(self, namefile, mode):
        with open(namefile, mode) as file:
            while True:
                data = self.send_to_server.recv(10_000)
                if not data:
                    break
                file = file.write(data)
                print(f'{namefile} received !')
