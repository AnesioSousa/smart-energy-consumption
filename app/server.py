#!/usr/bin/env python3

import routes.clientRoutes as Routes
import socket
from struct import *
import json
import os
from datetime import datetime
import threading


# O que vai rodar no processo principal? Já que to usando thread pra tudo?

MESSAGE_TYPE = "HH1024s"  # Regex?

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3

child_threads = []

# Tem que ter uma por tipo de conexão?

"""
cliente_id = 12345

    # Crie um diretório com o nome do cliente_id.


    # Salve os dados do cliente em um arquivo dentro do diretório.
    dados_do_cliente = {"nome": "João",
        "idade": 30, "email": "joao@example.com"}
    arquivo = os.path.join(diretorio, "dados.json")
    with open(arquivo, "w") as f:
        json.dump(dados_do_cliente, f)
"""


def recv_until(sock, suffix):
    message = sock.recv(4096)

    if not message:
        raise EOFError('socket closed')

    while not message.endswith(suffix):
        data = sock.recv(4096)
        if not data:
            raise IOError('received {!r} then socket closed'.format(message))
        message += data

    return message


def handle_client_tcp(self):

    while True:
        client, tcp_address = self.tcp_socket.accept()
        print(client.getpeername())

        """
        SERÁ QUE ESSE FUNCIONA?
        threading.Thread(target=send_update, args=[CURRENT_CONSUMN,
                     sock, refresh_time_queue]).start()
        
        """
        tcp_thread = threading.Thread(
            target=handle_client_tcp, args=[client, tcp_address])
        tcp_thread.start()

        request = client.recv(1024)
        print('Received TCP request from {}:'.format(address))
        response = Routes.handle_tcp_request(request)
        client.sendall(response.encode())

# ONDE ENTRAM AS QUEUES?


def handle_client_udp(self):

    while True:
        data, address = self.udp_socket.recvfrom(1024)
        thread = threading.Thread(
            target=handle_client_udp, args=[socket, data, address])
        thread.start()

    print('Received UDP request from: {}'.format(address))
    json_data = json.loads(data)
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
    print(
        f"Thread {current_thread.name} is handling client {address}")

# TENHO QUE ORQUESTRAR O MOVIMENTO COM AS LINHAS DE EXECUÇÃO PARALELAS (THREADS)


class Server(object):
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def main():
    HOST = 'localhost'
    TCPPORT = 65136
    UDPPORT = 65120
    MAX_BYTES = 65535

    my_dict = {}
    my_server = Server()

    try:
        my_server.tcp_socket.bind((HOST, TCPPORT))
        my_server.tcp_socket.listen()
        # print(f"Listening for TCP connections on {tcp_socket.getsockname()}")

        my_server.udp_socket.bind((HOST, UDPPORT))
        print(
            f"Listening for UDP messages on {my_server.udp_socket.getsockname()}")

    except Exception as exc:
        # Raise? KeyboardInterrupt
        print('\nNão foi possível iniciar o servidor!\nException: %s' % exc)

    udp_thread = threading.Thread(target=handle_client_udp, args=[])
    udp_thread.start()

    tcp_thread = threading.Thread(target=handle_client_tcp, args=[])
    tcp_thread.start()

    """
    if ("id_sensor", id) not in my_dict.items():
        
        
            # lidar com threads aqui
    
    """

    """
    json_data = json.loads(data)
    id = json_data.get("id_sensor")

    # Testa se o servidor já tem um arquivo json desse cliente
    

    # Tem que testar para ver se já tem uma thread rodando com dados desse cliente

    thread = threading.Thread(target=handle_client_udp, args=[
                                udp_socket, data, udp_address])
    thread.start()
    """


main()
