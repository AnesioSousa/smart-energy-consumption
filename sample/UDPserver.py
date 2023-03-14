#!/usr/bin/env python3

import socket
import struct


MESSAGE_TYPE = "HH1024s"  # Regex?

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3


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
# Suponha que cada cliente tenha um identificador único, como um número ou nome.


def receive_message(mysocket):
    MAX_BYTES = 65535

    data, addr = mysocket.recvfrom(65535)

    # Unpack the message from the binary string
    message_type, payload_length, payload = struct.unpack('!iis', data)

    # Decode the payload from bytes to a string
    payload = payload[:payload_length].decode()

    # Return the message type, payload length, payload, and the address of the sender
    return message_type, payload_length, payload, addr


def main():
    HOST = 'localhost'
    UDPPORT = 65120
    MAX_BYTES = 65535

    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        UDPServerSocket.bind((HOST, UDPPORT))
        print(f'Server is running on: {UDPServerSocket.getsockname()}')
    except Exception as exc:
        print('exception: %s' % exc)
    finally:
        pass

    while True:
        message_type, payload_length, payload, addr = receive_message(
            UDPServerSocket)
        print(f"Received message type {message_type} from {addr}: {payload}")
    """
    print('The client at {} says {!r}'.format(address, text))
    text = 'Your data was {} bytes long'.format(len(data))
    data = text.encode('ascii')
    UDPServerSocket.sendto(data, address)    
    """


main()
