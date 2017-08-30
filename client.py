import socket
import time
import random
import sys
import pickle


class Client:

    def __init__(self, ip_server):

        self.ip_server = ip_server
        self.port = 12500
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", 5348))
        self.socket.setblocking(0)

    def rcv_data_server(self):

        try:
            data, info = self.socket.recvfrom(2048)  # we already have the info server
            data = pickle.loads(data)

        except BlockingIOError:
            data = []

        return data

    def send_to_server(self, data):

        data_dumped = pickle.dumps(data)

        try:
            self.socket.sendto(data_dumped, (self.ip_server, self.port))

        except BlockingIOError:
            pass






