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
            "id_sensor": "SNS331",
            "request_id": "HESOYAM",
            "refresh_time": refresh_time,
            "time_stamp": time.time(),
            "current_measurement": consumo
        })
        sock.send(json_data.encode())
        queue.put(refresh_time)
        time.sleep(refresh_time)

        print(consumo)
        print("Data was send!")


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
    sock.connect(('localhost', 65120))
    print("Sucessfully connected")
    print('The OS assigned me the address {}'.format(sock.getsockname()))

    # E o id da requisição?

    """
    text = f'1124 {calculate_consumn(5200, 10)} {sock.getsockname()}'
    """
    refresh_time_queue.put(5)
    threading.Thread(target=send_update, args=[CURRENT_CONSUMN,
                     sock, refresh_time_queue]).start()

    # Tempo padrao de envio de dados é 10 min

    data, address = sock.recvfrom(1024)  # Aceita requisições do servidor
    # Tratar aqui o tempo de update

    json_data = json.loads(data)
    time_to_take_measures = json_data.get('refresh_time')

    # Atualizo o tempo de refresh
    if (time_to_take_measures != 10):
        refresh_time_queue.put(time_to_take_measures)

    print('The server {} replied {!r}'.format(address, data))