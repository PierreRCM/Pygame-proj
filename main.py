
import pygame as pg
import os
from pygame.locals import *
import window_manager as wm
import game_objects as go
import client
import time

pg.init()
pg.display.init()
pg.key.set_repeat(10, 10)


class Main:
    """ class to handle all input of the player
        might create an option to change shortcut """

    def __init__(self):

        self.client = client.Client("10.101.2.28")
        self.screen = wm.Screen()
        self.player = go.Player()
        self.map = wm.Map(self.player)
        self.camera = wm.Camera(self.screen.resolution, self.map.image.get_size())
        self.input = pg.key.get_pressed()
        self.gameOn = True
        self.clock = pg.time.Clock()
        self.dt = 0

    def _set_mouse_motion(self):

        events = pg.event.get()

        for event in events:
            if event.type == MOUSEMOTION:

                self.camera.set_attr("mouse", list(pg.mouse.get_pos()))
                self.player.set_attr("mouse", list(pg.mouse.get_pos()))

    def game_loop(self):

        while self.gameOn:

            self.dt = self.clock.tick(50) / 1000
            data_loads = self.client.rcv_data_server()

            self.map.handle_new_data(data_loads)
            self._set_mouse_motion()

            self.player.set_attr("tick", self.dt)
            self.player.keys = pg.key.get_pressed()
            self.player.check_inputs()  # Todo: Try to find a way to avoid moving and rotation the player in this method

            self.input = pg.key.get_pressed()

            self.camera.set_attr("tick", self.dt)
            self.camera.check_mouse()
            self.camera.update()

            dict_new_sprites = self.map.add_sprites(self.player)  # Need player instance to check whether the player is shooting
            data = self._create_data(dict_new_sprites)

            # Updating / displaying on screen
            self.map.deduce_camera_shift(self.camera)
            self.map.check_borders(self.camera.get_attr("position"))
            self.map.update()
            self.map.render(self.screen.screen, self.camera.rect)

            self.screen.check_input(self.input)

            self.client.send_to_server(data)

            pg.display.update()
            pg.event.pump()
            self.gameOn = self.screen.window

    def _create_data(self, dict_new_sprites):

        dict = {}

        if self.player.fire:

            dict["Bullets"] = dict_new_sprites["Bullet"]

            self.player.fire = False

        dict["Players"] = dict_new_sprites["Player"]

        return dict


server_response = False
main = Main()
main.client.send_to_server(main.player)

while not server_response:

    response = main.client.rcv_data_server()

    if response == "launch":

        server_response = True

main.game_loop()

