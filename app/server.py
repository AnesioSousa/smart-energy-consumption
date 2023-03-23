#!/usr/bin/env python3

import routes.clientRoutes as Routes
import socket
from struct import *
import json
import os
from datetime import datetime
import threading
import concurrent.futures
import queue
import logging
import time
import user

class UDPConnectionThread(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.users = {}
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.socket.settimeout(1)
        print("Listening to UDP connections on {!r}".format(self.socket.getsockname()))

    def run(self):
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                
                json_data = json.loads(data)
                id = json_data.get('id_sensor')
                
                if id in self.users:
                    my_user = self.users[id]
                else:
                    my_user = user.User('User', 'Rua dos bobos, número 0', 'example@email.com', '123456')
                    self.users[id] = my_user
                    
                consumo = json_data.get('current_measurement')
                time_stamp = json_data.get('time_stamp')
                
                aux = (consumo, time_stamp)
                my_user.measurements.append(aux)
                
                print(self.users)
            except socket.timeout:
                pass

class TCPConnectionThread(threading.Thread):
    def __init__(self,  host, port):
        super().__init__()
        self.host = host
        self.port = port
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        print("Listening to TCP connections on {!r}".format(self.socket.getsockname()))
        #print(socket.gethostbyname(socket.gethostname()))

    def run(self):
        self.socket.settimeout(1)
        self.socket.listen()
        while True:
            try:
                # Accept incoming connections
                client_socket, client_address = self.socket.accept()
                
                # Submit the connection to the executor for handling
                thread = threading.Thread(target=self.handle_connection, args=[client_socket, client_address])
                thread.start()
                
            except socket.timeout:
                pass
    
    def handle_connection(self, client_socket, client_address):
        #Tem que verificar se ja existe
        print(f"New connection from {client_address}")

        # Receive data from the client
        data = client_socket.recv(1024)
        if not data:
            print(f"No data received from {client_address}")
        else:
            print('Received TCP request from {}:'.format(client_address))
            response = Routes.handle_tcp_request(data)
            client_socket.sendall(response.encode())

        # Close the client socket
        client_socket.close()
        

class Server():
    def __init__(self, host, udp_port, tcp_port):
        self.host = host
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp_connection_thread = UDPConnectionThread(self.host, self.udp_port)
        self.tcp_connection_thread = TCPConnectionThread(self.host, self.tcp_port)

    def start(self):
        self.udp_connection_thread.start()
        self.tcp_connection_thread.start()
    

def main():
    logging.basicConfig(level=logging.DEBUG,
                      format='[%(levelname)s] (%(threadName)-9s) %(message)s',)
    HOST = '172.16.103.208'
    TCPPORT = 65136
    UDPPORT = 65120

    my_server = Server(HOST, UDPPORT, TCPPORT)
    my_server.start()

main()
