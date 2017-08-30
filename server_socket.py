import socket
import time
import pickle
import os
import sys
import pygame as pg

print("Looking for your own IP...")
print("Intranet Protocol: {} \n".format(socket.gethostbyname(socket.gethostname())))
# Todo: I think that bullets are most of the time not receive because of the UDP sockets
# Todo: need to find a way to ensure that the client get the bullets
# Todo: aswell need to find a way to avoid Nonetype Error involved if the image dictionary is not set
# Todo: Why do i have a connexion error on an UDP socket, it only happen to the HOST when it disconnect.
# Todo: Handle bullets in the same way as player, the server nee to keep transfering bullets data to make sure
# Todo: that the bullet is on the other screen, and avoid udp packet lose
# Todo: Furthermore, each player object need an argument to deduce the motion of the camera on each sprite
# Todo: something like : self.camera_motion = [50, 30] and deduce on each sprite coming from the server.
# Todo: because each sprites are not in the same position on each screen.

class Server:
    """Server UDP socket"""
    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 12500
        self.socket.bind(("", self.port))
        self.clients = {}  # Client name and IP
        self.clients_number = len(self.clients)
        self.players = {}
        self.bullets = []
        self.new_bullet = None
        self.last_client = str()
        self.waiting_for_connexion = True

    def rcv_data(self):
        """Receive incoming data"""
        try:

            data, info_client = self.socket.recvfrom(2048)
            self.last_client = info_client

            self._handle_data(data)

        except BlockingIOError:  # Useless because method socket.setblocking(0) not used
            pass

    def send_data(self):
        """Transfer incoming data to all client except to the owner of the sprites"""

        for client_info, player_name in self.clients.items():

            data_to_send = [self.players.copy()]
            data_to_send[0].pop(player_name)

            if self.new_bullet is not None:
                if player_name != self.new_bullet.owner:

                    data_to_send.append(self.new_bullet)  # Todo: refer to packet losing in todo above

            data_to_send = pickle.dumps(data_to_send)

            self.socket.sendto(data_to_send, client_info)

    def _handle_data(self, data):
        """input data sent by the client, filter bullet and player, add bullet in a list, call check update
            to watch out if the player move"""

        data_loads = pickle.loads(data)

        if data_loads["Bullet"] is not None:

            self.bullets.append(data_loads["Bullet"])
            self.new_bullet = data_loads["Bullet"]

        self._check_update(data_loads["Player"])

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
                self.players[player.name] = player
                print("Client : " + info_client[0] + " successfully added to client list \n")

            if len(self.clients) == 2:

                self.waiting_for_connexion = False

        except BlockingIOError:
            pass

    def launch_game(self):

        print("GAME STARTING")
        message = pickle.dumps("launch")

        for info_client in self.clients.keys():
            print(info_client)
            self.socket.sendto(message, info_client)

    def _check_update(self, player):
        """input player instance, if player rect on the server in not the same that on the client, update server"""

        player_rect = self.players[player.name].rect

        if player_rect != player.rect:
            self.players[player.name] = player

    def update_bullets(self, dt):

        for bullet in self.bullets:
            bullet.update(dt)

    def check_alive(self):

        for bullet in self.bullets:

            if not bullet.get_attr("alive"):

                self.bullets.remove(bullet)

server = Server()

while server.waiting_for_connexion:

    server.save_connexion()

server.launch_game()

# dt = pg.time.get_ticks()

while 1:

    # dt = pg.time.get_ticks()
    server.rcv_data()
    server.send_data()
    # server.update_bullets(dt)  # On the server, the screen is not init, so there is no way to work with surface
    # server.check_alive()
    # print(len(server.bullets))
