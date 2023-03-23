#!/usr/bin/env python3

import routes.clientRoutes as Routes
import socket
from struct import *
import json
from datetime import datetime
import threading
import logging
import user

users = {}


def handle_tcp_request(request):
        request = request.decode()
        fields = request.split('\r\n')
        method, path, version = fields[0].split(' ')

        headers = {}
        for field in fields[1:]:
            if field == '':
                break
            key, value = field.split(': ')
            headers[key] = value

        content_type = headers.get('Content-Type')
        content_length = int(headers.get('Content-Length', 0))

        # Parsea o corpo da requisição se ele existe e se é do tipo JSON
        body = ''
        if content_length > 0 and content_type == 'application/json':
            body = json.loads(fields[-1])

        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: application/json\r\n"
        response += "\r\n"
        response += get_response_data(method, path)

        return response
    
def get_response_data(method, path):
    if method == 'GET' and path == '/':
        # definir consumo
        return json.dumps({'message': 'Welcome to the SmartMeter API!'})
    elif method == 'GET' and path == '/activeMonitors':
        # broadcast
        
        aux ={}
        for user in users.values():
            user_data = user.toJSON()
            aux.update(user_data)
        return json.dumps(aux)

    elif method == 'POST' and path == '/calcularFatura/id':
        
        # Pede o id do monitor e a quantidade de dias. Retorna a fatura em formato Json
        return json.dumps({'counter': "123"})
    elif method == 'POST' and path == '/api/smartmeter/id':
        # definir consumo
        data = path.split('/')
        print(data)
        return json.dumps({'status': 'ok',
                        "SmartMeter_ID": id})
    elif method == 'PUT' and path == '/api/smartmeter':
        # aumentar consumo

        return json.dumps({'status': 'ok'})
    elif method == 'PUT' and path == '/api/smartmeter':
        # diminuir consumo
        return json.dumps({'status': 'ok'})
    else:
        return json.dumps({'error': 'Invalid request.'})

class UDPConnectionThread(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
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
                
                if id in users:
                    my_user = users[id]
                else:
                    my_user = user.User('User', 'Rua dos bobos, número 0', 'example@email.com', '123456')
                    users[id] = my_user
                    
                consumo = json_data.get('current_measurement')
                time_stamp = json_data.get('time_stamp')
                
                aux = (consumo, time_stamp)
                my_user.measurements.append(aux)
                
                print(json_data)
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
            response = handle_tcp_request(data)
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
