#!/usr/bin/env python3
import struct
import json

routes = {}


def route(path):
    def wrapper(handler):
        routes[path] = handler
        return handler
    return wrapper


@route('/')
def index_handler():
    return '<h1>Welcome to my website!</h1>'


@route('/about')
def about_handler():
    return '<h1>About us</h1><p>We are a small company that loves to make websites.</p>'


@route('/contact')
def contact_handler():
    return '<h1>Contact us</h1><p>Email: info@example.com</p><p>Phone: 555-1234</p>'


@route('/api/smartmeter')
def data_handler():
    return '{"data": [1, 2, 3, 4, 5]}'


def not_found():
    return 'Page not found', 404

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

    """
    elif method == 'PUT' and path = '/login':
        # logar user
        return json.dumps({query_params[]})
    """


def handle_tcp_request(request):
    """
    handler = routes.get(path, not_found)
    response, status = handler()
    """

    lines = request.split('\n')
    method, path, version = lines[0].split(' ')

    headers = {}
    for line in lines[1:]:
        print(line)
        if line == '':
            break
        key, value = line.split(': ')
        headers[key] = value
    content_type = headers.get('Content-Type')
    content_length = int(headers.get('Content-Length', 0))

    # Parsea o corpo da requisição se ele existe e se é do tipo JSON
    body = ''
    if content_length > 0 and content_type == 'application/json':
        body = json.loads(lines[-1])

    response = "HTTP/1.1 200 ok\r\n"
    response += "Content-Type: text/html\r\n"
    response += "\r\n"
    response += get_response_data(method, path, body)

    return response


def handle_udp_request(request):
    # Unpack the message from the binary string
    message_type, payload_length, payload = struct.unpack('!iis', request)
