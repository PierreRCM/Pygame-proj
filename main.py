import pygame as pg
import os
from pygame.locals import *
import window_manager as wm
import game_objects as go
import client

pg.init()
pg.display.init()
pg.key.set_repeat(10, 10)


class Main:
    """ class to handle all input of the player
        might create an option to change shortcut """

    def __init__(self):

        self.client = client.Client()
        self.screen = wm.Screen()
        self.player = go.Player()
        self.map = wm.Map({"a": pg.sprite.Group(self.player), "p": pg.sprite.Group()})
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

        self.client.connect()

        while self.gameOn:

            self.dt = self.clock.tick(50) / 1000

            self._set_mouse_motion()

            self.player.set_attr("tick", self.dt)
            self.player.keys = pg.key.get_pressed()
            self.player.check_inputs()

            self.input = pg.key.get_pressed()

            self.camera.set_attr("tick", self.dt)
            self.camera.check_mouse()
            self.camera.update()

            self.map.add_sprites(self.player)
            self.map.deduce_camera_shift(self.camera)
            self.map.check_borders(self.camera.get_attr("position"))
            self.map.update()
            self.map.render(self.screen.screen, self.camera.rect)

            self.screen.check_input(self.input)

            self.gameOn = self.screen.window
            self.client.send_data(self.map.groupe_dict)

            pg.display.update()
            pg.event.pump()

main = Main()
main.game_loop()
