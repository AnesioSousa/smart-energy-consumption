#!/usr/bin/env python3

import socket
from datetime import datetime
import time
import json
import threading
import queue


eletrodomesticos = {
    "Lampada Philco": 4,
    "Liquidificador": 1200
}

"""
potency: watt (W)
time: minutes (min)

"""

def calculate_consumn(potency, time):
    converted_time = time/60  # Convert minutes to hours
    converted_power = potency/1000  # Convert Watts to kiloWatts
    return converted_power*converted_time


def send_update(consumo, sock, queue):
    is_connected = True

    while is_connected:
        # Cuidado, tem que ser menor que o tempo definido de update
        refresh_time = queue.get(timeout=1)
        if refresh_time == 0:
            return

        consumo += calculate_consumn(5200, refresh_time)

        json_data = json.dumps({
            "id_sensor": "SNS554",
            "current_measurement": consumo,
            "time_stamp": time.time()
        })
        sock.send(json_data.encode())
        queue.put(refresh_time)

        time.sleep(refresh_time)


def get_total_consumn(time):
    # Calcula e soma o consumo com tudo ligado pelo tempo que tá setado do obj, que pode ter sido setado tanto pelo server via a API HTTP, tando diretamente (Que ainda falta criar
    # )
    for k, v in eletrodomesticos.items():
        print(k, v)

    CURRENT_CONSUMN += calculate_consumn()
    return  # consumo toal


if __name__ == '__main__':
    """
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)

    """
    CURRENT_CONSUMN = 0
    refresh_time_queue = queue.Queue()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(('172.16.103.208', 65120))
    print("Sucessfully connected")
    print('The OS assigned me the address {}'.format(sock.getsockname()))

    refresh_time_queue.put(10)
    threading.Thread(target=send_update, args=[CURRENT_CONSUMN,
                     sock, refresh_time_queue]).start()

    # Tempo padrao de envio de dados é 10 segundos
    # Não é melhor usar o connect?
    # Usar thread aqui
    data, address = sock.recvfrom(1024)  # Aceita requisições do servidor
    # Tratar aqui o tempo de update
    
