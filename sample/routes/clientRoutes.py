#!/usr/bin/env python3

# Lembrar de fazer um comando para todas as máquinas que estão conteinerizadas apontarem para o endereço do meu servidor
import struct
import json

# Esse cara tem que lidar com múltiplos protocolos


def get_response_data(method, path, query_params):
    if method == 'GET' and path == '/api/smartmeter':
        return json.dumps({'counter': "123"})
    elif method == 'POST' and path == '/api/smartmeter':
        # definir consumo

        return json.dumps({'status': 'ok'})
    elif method == 'PUT' and path == '/api/smartmeter':
        # aumentar consumo

        return json.dumps({'status': 'ok'})
    elif method == 'PUT' and path == '/api/smartmeter':
        # diminuir consumo
        return json.dumps({'status': 'ok'})
    else:
        return json.dumps({'error': 'Invalid request.'})


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
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += get_response_data(method, path, body)

    return response


def handle_udp_request(request):
    # Unpack the message from the binary string
    message_type, payload_length, payload = struct.unpack('!iis', request)

    print(f"Received message type {message_type} from Teste: {payload}")
