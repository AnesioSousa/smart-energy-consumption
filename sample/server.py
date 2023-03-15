#!/usr/bin/env python3

import routes.clientRoutes as Routes
import threading
import socket
import json


# O que vai rodar no processo principal? Já que to usando thread pra tudo?


MESSAGE_TYPE = "HH1024s"  # Regex?

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3

child_processes = []

# Tem que ter uma por tipo de conexão?


"""
    cliente_id = 12345

    # Crie um diretório com o nome do cliente_id.
    diretorio = f"./clientes/{cliente_id}"
    os.makedirs(diretorio, exist_ok=True)

    # Salve os dados do cliente em um arquivo dentro do diretório.
    dados_do_cliente = {"nome": "João", "idade": 30, "email": "joao@example.com"}
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


def handle_client_udp(socket, data, address):
    with socket:
        request = data.decode()
        print('\n')
        print('Received UDP request from: {}'.format(address))
        print(request)
        response = Routes.handle_udp_request(request)
        socket.sendto(response.encode(), address)


def main():
    HOST = 'localhost'
    TCPPORT = 65136
    UDPPORT = 65120
    MAX_BYTES = 65535

    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Pra não deixar conexão. Quando o processo morrer fecha tudo
    tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:

        tcp_socket.bind((HOST, TCPPORT))
        tcp_socket.listen()
        print(f"Listening for TCP connections on {tcp_socket.getsockname()}")

        udp_socket.bind((HOST, UDPPORT))
        print(f"Listening for UDP messages on {udp_socket.getsockname()}")

    except Exception as exc:
        # Raise?
        print('\nNão foi possível iniciar o servidor!\nException: %s' % exc)

    while True:
        client, tcp_address = tcp_socket.accept()
        thread = threading.Thread(
            target=handle_client_tcp, args=[client, tcp_address])
        thread.start()
        print(threading.active_count())

        """
        data, udp_address = udp_socket.recvfrom(1024)
        thread = threading.Thread(target=handle_client_udp, args=[
                                  udp_socket, data, udp_address])
        thread.start()
        
        
        """


main()
