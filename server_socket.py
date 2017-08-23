import socket
import time
import pickle
import os
import sys


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
        self.new_bullet = None
        self.players = {}
        self.bullets = []
        self.last_client = str()
        self.waiting_for_connexion = True

    def rcv_data(self):
        """Receive incoming data"""
        try:

            data, info_client = self.socket.recvfrom(2048)
            self.last_client = info_client

            self._handle_data(data)

        except BlockingIOError or OSError:  # Todo: find a way to remove those try ( no data and overload buffer)
            pass

    def send_data(self):
        """Transfer incoming data to all client except to the owner of the sprites"""

        for client_info, player_name in self.clients.items():

            data_to_send = [self.players]
            data_to_send[0].pop(player_name)



            self.socket.sendto(data_to_send, client_info)

        self.new_bullet = None

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

    def _handle_data(self, data):
        """input data sent by the client, filter bullet and player, add bullet in a list, call check update
            to watch out if the player move"""
        data_loads = pickle.loads(data)

        for type_sprite, sprite in data_loads.items():

            if isinstance(type_sprite, go.Bullet):

                self.new_bullet = sprite
                self.bullets.append(sprite)

            elif isinstance(type_sprite, go.Player):

                self._check_update(sprite)

    def _check_update(self, player):
        """input player instance, if player rect on the server in not the same that on the client, update server"""

        player_rect = self.players[player.name].rect

        if player_rect != player.rect:

            self.players[player.name] = player

    def save_connexion(self):

        try:

            data, info_client = self.socket.recvfrom(2048)
            self.last_client = info_client

            if not (info_client in self.clients.keys()):

                print("{}: First connexion".format(info_client))
                print("Saving client information... \n")
                player = pickle.loads(data)
                self.clients_number += 1
                self.clients[info_client] = player.name
                self.clients_last_call[info_client] = time.time()
                self.players[player.name] = player
                print("Client : " + info_client[0] + " successfully added to client list \n")

            if len(self.clients) != 0:

                self.waiting_for_connexion = False

        except BlockingIOError:
            pass

    def launch_game(self):

        print("LAUNCHING GAME")
        message = pickle.dumps("launch")
        for info_client in self.clients.keys():

            self.socket.sendto(message, info_client)


server = Server()

while server.waiting_for_connexion:

    server.save_connexion()

server.launch_game()

while 1:

    server.rcv_data()
    server.check_list()
    server.send_data()

