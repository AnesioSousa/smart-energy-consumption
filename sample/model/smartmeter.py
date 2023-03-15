
import random
import string
import time
import datetime
import socket
import struct
from enum import Enum

# IDEIA: Criar uma fábrica de eletrodomesticos e associar a um medidor. Em tempo de execução poder ligá-los (individualmente) e ver a alteração na conta
MESSAGE_FORMAT = "HH1024s"


Message = Enum('MESSAGE_TYPE', ['HELLO', 'DATA', 'GOODBYE'])

MESSAGE_TYPE_HELLO = 1
MESSAGE_TYPE_DATA = 2
MESSAGE_TYPE_GOODBYE = 3


class SmartMeter:
    @classmethod
    def __init__(self, host, port, macAddress=-1):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port
        self.macAddress = macAddress
        self.serialNumber = ''.join(random.choices(
            string.ascii_letters + string.digits, k=32))
        self.myMeasurement = self.Measurement()
        self.client_socket.connect((host, port))

    @classmethod
    def getMeasurement(self):
        return self.myMeasurement.startSensing()

    @classmethod
    def sendMeasure(self, addr, message_type):
        while True:
            print("HELL YEAH!")
            data = 'Counter value: {} kWh'.format(self.myMeasurement.value)

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
    def connect(self):
        self.client_socket.connect((self.host, self.port))

    @classmethod
    def getSerialNumber(self):
        return self.serialNumber

    class Measurement:
        @classmethod
        def __init__(self):
            self.__value = 0
            self.time_stamp = None
            self.lastMeasurement = 0
            self.lastMeasurementTimeStamp = 0
            self.isMeasuring = True
            self.startSensing()

        # private method incluir os cálculos das potências aqui
        @classmethod
        def startSensing(self):
            time.sleep(1)
            self.isMeasuring = True
            self.value += 5

        @property
        def value(self):
            return self.__value

        @classmethod
        def stopSensing(self):
            self.isMeasuring = False

        @classmethod
        def __del__(self):
            print("Object is being destroyed with counter value:", self.value)

        @property
        def measure(self, time):
            med = self.value - self.lastMeasurement
            self.lastMeasurement = self.value
            self.lastMeasurementTimeStamp = datetime.datetime.now()
            return (med, self.lastMeasurementTimeStamp)
