import unittest
import socket

from sample import *

HOST = "127.0.0.1"
PORT = 65432
timeout_seconds = 1


class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def test_server_disconnection(self):
        server = SimpleServer
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(timeout_seconds)
        result = self.client.connect_ex((HOST, int(PORT)))
        if result == 0:
            print("Host: {}, Port: {} - True".format(HOST, PORT))
        else:
            print("Host: {}, Port: {} - False".format(HOST, PORT))
        self.client.close()

    def test_sum_tuple(self):
        self.assertEqual(sum([1, 2, 2]), 6, "Should be 6")


if __name__ == "__main__":
    unittest.main()
