#!/usr/bin/env python3

import routes.clientRoutes as Routes
import threading
import time
import socket
from struct import *
import json
import os
from datetime import datetime


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


def handle_client_tcp(client, address):
    with client:
        request = client.recv(1024)
        print('Received TCP request from {}:'.format(address))
        response = Routes.handle_tcp_request(request)
        client.sendall(response.encode())

# ONDE ENTRAM AS QUEUES?


def handle_client_udp(socket, data, address):
    is_connect = True

    with socket:
        print('Received UDP request from: {}'.format(address))
        json_data = json.loads(data)
        time_to_take_measures = json_data.get('refresh_time')
        current_measurement = json_data.get('current_measurement')

        print(f"Time between measurements: %s seconds" %
              time_to_take_measures)
        print(f"Medição {current_measurement} kWh")

# TENHO QUE ORQUESTRAR O MOVIMENTO COM AS LINHAS DE EXECUÇÃO PARALELAS (THREADS)


def main():
    HOST = 'localhost'
    TCPPORT = 65136
    UDPPORT = 65120
    MAX_BYTES = 65535

    my_dict = {}

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Pra não deixar conexão. Quando o processo morrer fecha tudo
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:

        tcp_socket.bind((HOST, TCPPORT))
        tcp_socket.listen()
        # print(f"Listening for TCP connections on {tcp_socket.getsockname()}")

        udp_socket.bind((HOST, UDPPORT))
        print(f"Listening for UDP messages on {udp_socket.getsockname()}")

    except Exception as exc:
        # Raise? KeyboardInterrupt
        print('\nNão foi possível iniciar o servidor!\nException: %s' % exc)

    while True:
        """
        client, tcp_address = tcp_socket.accept()
        print(client.getpeername())
        thread = threading.Thread(
            target=handle_client_tcp, args=[client, tcp_address])
        thread.start()
        """

        data, udp_address = udp_socket.recvfrom(1024)

        # Salva os dados do cliente em um arquivo dentro do diretório.

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
