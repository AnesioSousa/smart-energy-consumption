#!/usr/bin/env python3

from TCPserver import Server
from sensor import Sensor
from controllers.httpParser import HttpParser
import threading
import http.server
import socketserver

if __name__ == '__main__':

    my_server = Server('localhost', 65301)
    my_server.start_listening()

    parser = HttpParser()
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", 65301), Handler) as httpd:
        print("serving at port", 65301)
        httpd.serve_forever()
