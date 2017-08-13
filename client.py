import socket
import time
import random
import sys
import pickle

class Client:

    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ip = "192.168.1.107"
        self.port = 12150

    def connect(self):

        print("connecting to : " + self.ip + " on port : " + str(self.port)+ "...")
        self.socket.connect((self.ip, 12150))
        print("Connection successful")

    def send_data(self, data):

        data = pickle.dumps(data)

        self.socket.send(data)





