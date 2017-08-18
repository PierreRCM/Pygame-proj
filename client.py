import socket
import time
import random
import sys
import pickle

# class Client:
#
#     def __init__(self):
#
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.ip = "192.168.0.4"
#         self.port = 12150
#         self.data_rcv = None
#
#     def connect(self):
#
#         print("connecting to : " + self.ip + " on port : " + str(self.port)+ "...")
#         self.socket.connect((self.ip, 12150))
#         print("Connection successful")
#
#     def send_data(self, data):
#
#         data = pickle.dumps(data)
#
#         self.socket.send(data)
#
#     def rcv_data(self):
#
#         try:
#             self.data_rcv = self.socket.recv(4096)
#             self.data_rcv = pickle.loads(self.data_rcv)
#
#         except:
#             pass
#


class Client:

    def __init__(self, ip_server):

        self.ip_server = ip_server
        self.port = 12500
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def rcv_data_server(self):

        data, info_server = self.socket.recvfrom(4096)  # we already have the info server

        data_loads = []  # might do a for loop to handle several package coming at once

        for data_list in data:

            data_loads.append(pickle.loads(data_list))

        return data_loads  # dataloads is a list of a list which contain sprites

    def send_to_server(self, data):

        data_dumped = pickle.dumps(data)
        self.socket.sendto(data_dumped, (self.ip_server, self.port))

