import socket
import time
import pickle
import pygame as pg

class Server:

    def __init__(self):

        self.ip = socket.gethostname()
        self.port = 12150
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connexion = None
        self.info_co = None
        self.data_rcv = None
        self.myUnpickle = pickle.Unpickler

    def listen(self):

        self.socket.bind(("", self.port))
        print("Socket listening...")
        self.socket.listen(5)
        print("Waiting for connexion...")
        self.connexion, self.info_co = self.socket.accept()
        print(str(self.info_co)+ " just connect !")

    def rcv_data(self):

        self.data_rcv = self.connexion.recv(4096)
        try:
            self.data_rcv = pickle.loads(self.data_rcv)
        except:
            pass


    def send_data(self, data):

        data = pickle.dumps(data)

        self.socket.send(data, (self.info_co))



server = Server()
server.listen()

while True:

    server.rcv_data()
    print(server.data_rcv)
