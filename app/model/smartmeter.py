
import random
import string
import time
import datetime
import socket
import struct
import sys
from enum import Enum
import threading
import argparse

# IDEIA: Criar uma fábrica de eletrodomesticos e associar a um medidor. Em tempo de execução poder ligá-los (individualmente) e ver a alteração na conta
MESSAGE_FORMAT = "HH1024s"


Message = Enum('MESSAGE_TYPE', ['HELLO', 'DATA', 'GOODBYE'])

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3


class SmartMeter(object):
    @classmethod
    def __init__(self, host, port):
        self.my_measurement = self.Measurement()
        self.host = host
        self.port = int(port)

    """"""
    @classmethod
    def create_connection(self, hostname, port, time):  # Se já tem um hostname vindo
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = socket.gethostbyname(hostname)

        hostname = sys.argv[2]  # Pra que substuir o que vem?
        my_socket.connect((hostname, port))
        time.sleep(time)
        consumo_em_kWh = self.calculate_consumn()
        text = 'This is another message'
        data = text.encode('ascii')
        while True:
            my_socket.send(data)
            print('Waiting up to {} seconds for a reply'.format(delay))
            my_socket.settimeout(delay)
            try:
                data = my_socket.recv(1024)
            except socket.timeout:
                delay *= 2  # wait even longer for the next request
                if delay > 2.0:
                    raise RuntimeError('I think the server is down')
                else:
                    break  # we are done, and can stop looping

            print('The server says {!r}'.format(data.decode('ascii')))

    def send_data(self, my_socket, text, destination):
        data = text.encode('ascii')
        my_socket.sendto(destination, data)

    """
    potency - Watts
    time - Minutos
    """
    @classmethod
    def calculate_consumn(self, potency, time):
        converted_time = time/60
        converted_power = potency/1000
        return converted_power*converted_time

    @classmethod
    def calculate_total_consumn(self, time):
        # Pra cada item no dicionário, calcular a sua potencia, somá-las e retornar a total
        pass

    # private method
    @classmethod
    def generate_request_id():
        return ''.join(random.choices(
            string.ascii_letters + string.digits, k=32))

    @classmethod
    def sendMeasure(self, addr, message_type, time):
        while True:
            print("HELL YEAH!")
            data = 'Counter value: {} kWh'.format(self.myMeasurement.value)
            time.sleep(time)
            message = struct.pack('!iis', message_type,
                                  len(data), data.encode('ascii'))
            # É melhor usar sendall() ou sendoto()?
            self.client_socket.sendto(message, addr)

            # Verificar se a conexão foi fechada pelo servidor
            # Criar uma melhor condição de paradaAqui já entra as questões do livro sobre clientes promiscuos e etc
            response = self.client_socket.recv(1024)
            if not response:
                break

    @classmethod
    def getSerialNumber(self):
        return self.serialNumber
    """
    # É como o toString do Java!
    @classmethod
    def __repr__(self):
        return f"Meter(email={self.nome}, senha={self.idade}, serial={self.altura})"
    
    """

    class Measurement(object):
        @classmethod
        def __init__(self):
            self.__value = 0
            self.time_stamp = None
            self.lastMeasurement = 0
            self.lastMeasurementTimeStamp = 0
            self.isMeasuring = True

        # private method incluir os cálculos das potências aqui
        @classmethod
        def startSensing(self):
            time.sleep(1)
            self.value += 5

        @classmethod
        def stopSensing(self):
            self.isMeasuring = False

        @classmethod
        def __del__(self):
            print("Object is being destroyed with counter value:", self.value)

        @property
        def value(self):
            return self.__value

        @ property
        def measure(self, time):
            med = self.value - self.lastMeasurement
            self.lastMeasurement = self.value
            self.lastMeasurementTimeStamp = datetime.datetime.now()
            return (med, self.lastMeasurementTimeStamp)


if __name__ == '__main__':
    my_meter = SmartMeter()
    my_meter.create_connection('localhost', 1060, 10)
