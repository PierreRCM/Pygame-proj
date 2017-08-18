import socket
import time
import pickle
import os
import sys

# class Server:
#
#     def __init__(self):
#
#         self.ip = socket.gethostname()
#         self.port = 12150
#         self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.socket.bind(("", self.port))
#         self.connexion = []
#         self.info_co = []
#         self.data_rcv = None
#         self.myUnpickle = pickle.Unpickler
#
#     def listen(self):
#
#
#         print("Socket listening...")
#         self.socket.listen(5)
#         print("Waiting for connexion...")
#         connexion, info_co = self.socket.accept()
#         self.connexion.append(connexion)
#         self.info_co.append(info_co)
#         print(str(info_co)+ " just connect !")
#
#     def rcv_data(self):
#
#         self.data_rcv = self.connexion[0].recv(4096)
#         try:
#             self.data_rcv = pickle.loads(self.data_rcv)
#         except:
#             pass
#         print(self.data_rcv)
#         self._send_data(self.data_rcv)
#
#     def _send_data(self, data):
#
#         data = pickle.dumps(data)
#
#         self.connexion[1].send(data)
#
#
#
# server = Server()
# server.listen()
# server.listen()
#
# while True:
#
#     server.rcv_data()
#

print("Looking for your own IP...")
print("Intranet Protocol: {} \n".format(socket.gethostbyname(socket.gethostname())))

class Server:
    """Server UDP socket"""
    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 12500
        self.socket.bind(("", self.port))
        self.clients = {}  # Client name and IP
        self.clients_number = len(self.clients)
        self.clients_last_call = {}
        self.socket.setblocking(0)

    def rcv_data(self):

        try:

            data, info_client = self.socket.recvfrom(4096)

            if not (info_client[0] in self.clients.keys()):

                print("{}: First connexion".format(info_client[0]))
                print("Saving client connexion information... \n")
                self.clients_number += 1
                self.clients[info_client[0]] = self.clients_number
                self.clients_last_call[info_client[0]] = time.time()
                print("Client : " + info_client[0] + " successfully added to client list \n")


            self._send_data(data, info_client)

        except BlockingIOError:
            pass


    def _send_data(self, data, info_client):
        """Transfer incoming data to all client except the on who send it"""

        clients_list = self.clients.copy()
        clients_list_to_send = clients_list.pop(info_client[0])

        for client_ip in clients_list_to_send.keys():

            self.socket.sendto(data, (client_ip, self.port))

    def check_list(self):
        """ After a time the information of the client are removed, think it's useless as we get it back when
            he ll be back """

        clients_last_call_dict = self.clients_last_call.copy()

        for client, client_last_call in clients_last_call_dict.items():

            if time.time() - client_last_call > 5.0:

                print("Client {} does not send anymore data".format(client))
                self.clients.pop(client)
                self.clients_number -= 1
                self.clients_last_call.pop(client)
                print("Client {} data removed\n".format(client))



server = Server()

while 1:

    server.rcv_data()
    server.check_list()


