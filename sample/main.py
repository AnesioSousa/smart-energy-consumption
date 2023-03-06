from server import Server
from sensor import Sensor
from controller.httpParser import HttpParser
import threading

if __name__ == '__main__':

    my_sensor = Sensor('localhost', 65301)
    my_sensor.connect()
    my_server = Server('localhost', 65301)
    my_server.start_listening()
