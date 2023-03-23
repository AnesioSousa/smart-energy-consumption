#!/usr/bin/env python3

# Lembrar de fazer um comando para todas as máquinas que estão conteinerizadas apontarem para o endereço do meu servidor
import json

# Esse cara tem que lidar com múltiplos protocolos


def get_response_data(method, path, query_params):
    if method == 'GET' and path == '/':
        # definir consumo
        return json.dumps({'message': 'Welcome to the SmartMeter API!'})
    elif method == 'GET' and path == '/activeMonitors':
        # broadcast

        return

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
    response += get_response_data(method, path, body)

    return response
