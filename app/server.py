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

# O que vai rodar no processo principal? Já que to usando thread pra tudo?

MESSAGE_TYPE = "HH1024s"  # Regex?

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3

class UDPConnectionThread(threading.Thread):
    def __init__(self, host, port, executor):
        super().__init__()
        self.host = host
        self.port = port
        self.executor = executor
        self.connected_sensors = {}
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
                
                
                if self.connected_sensors.get(id) is not None:
                    """
                    Se tem medida, mas não atualiza, ou existe a thread mas não dá pra se comunicar no endereço dela:
                    #reconexão - Atualizar o endereço da thread do cliente
                    print(f"The sensor {id} is reconnected")
                    """
                    pass
                else:
                    print("New Connection!")
                    #Acho que ele tem que mandar um Signal pra thread pegar o novo valor
                    data_queue = queue.Queue()
                    data_queue.put(data)
                    
                    my_receiver = self.Receaver(address, data_queue)
                    self.connected_sensors[id] = my_receiver
                    my_receiver.start()
                    print(threading.active_count())
                
                    
                    

            except socket.timeout:
                pass
            
    class Receaver(threading.Thread):
        def __init__(self, address, queue):
            super().__init__()
            self.queue = queue
            self.measures = []
            self.address = address
            
        def run(self):
            data = self.queue.get(timeout=1)
            
            if not data:
                print("Algo de errado não está certo!")
            
            print(f"Received UDP data -> {data.decode()} from {self.address}")
            # Do something with the data and address
            
            #response = "Hello from server"
            
            #LEMBRA QUE TEM QUE ENVIAR JSONS AQUI
            #self.socket.sendto(response.encode(), self.address)

        
        def get_sensor_id(self):
            return self.id_sensor
        
        class Message:
            def __init__(self, data, address):
                self.data = data
                self.address = address
            
            
            def get_data(self):
                return self.data
            
            def get_address(self):
                return self.address
    

class TCPConnectionThread(threading.Thread):
    def __init__(self,  host, port,executor):
        super().__init__()
        self.host = host
        self.port = port
        self.executor = executor

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
                self.executor.submit(self.handle_connection, client_socket, client_address)
                
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
    def __init__(self, host, udp_port, tcp_port, num_threads=10):
        self.host = host
        self.udp_port = udp_port
        self.tcp_port = tcp_port
        self.udp_executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.tcp_executor = concurrent.futures.ThreadPoolExecutor(max_workers=num_threads)
        self.udp_connection_thread = UDPConnectionThread(self.host, self.udp_port, self.udp_executor)
        self.tcp_connection_thread = TCPConnectionThread(self.host, self.tcp_port, self.tcp_executor)

    def start(self):
        self.udp_connection_thread.start()
        self.tcp_connection_thread.start()
        
        
    """

    def handle_client_udp(self):
        
        while True:
            
            data, address = self.udp_socket.recvfrom(1024)
            json_data = json.loads(data)
            id = json_data.get("id_sensor")
            
            if(threading.)
            
            
            
            senser = SmartSenser(address, data, address)
            t = MyThread(senser, 5)
            t.start()
            
            
            thread = threading.Thread(
                target=handle_client_udp, args=[data, address])
            thread.start()

        print('Received UDP request from: {}'.format(address))
        
        time_to_take_measures = json_data.get('refresh_time')
        current_measurement = json_data.get('current_measurement')

        print(f"Time between measurements: %s seconds" %
            time_to_take_measures)
        print(f"Medição {current_measurement} kWh")

        dados_do_cliente = json.loads(data)
        id = dados_do_cliente.get("id_sensor")
        time_stamp = dados_do_cliente.get("time_stamp")
        date_time = datetime.fromtimestamp(time_stamp)
        print(date_time)

        diretorio = f"./monitors/{id}"
        arquivo = os.path.join(diretorio, f"{time_stamp}.json")
        os.makedirs(diretorio, exist_ok=True)
        with open(arquivo, "w") as f:
            json.dump(dados_do_cliente, f)

        current_thread = threading.current_thread()
        print(f"Thread {current_thread.name} is handling client {address}")
    
    
    
    """
    

def main():
    HOST = '172.16.103.208'
    TCPPORT = 65136
    UDPPORT = 65120

    my_server = Server(HOST, UDPPORT, TCPPORT)
    my_server.start()


main()
