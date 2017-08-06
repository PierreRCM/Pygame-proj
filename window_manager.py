import pygame as pg
import os
import object_interaction_manager as oim
pg.init()

size_window = (800, 600)
screen = pg.display.set_mode(size_window)
background = pg.image.load(os.getcwd() + "\\picture\\map.jpg")

class Camera:

    def __init__(self, screen_size, background):

        self.image = background
        self.screen_size = screen_size
        self.rect = pg.Rect((0, 0) , screen_size)
        self._attr = {"mouse": [0, 0], "speed": 400, "tick": 0, "position": [0, 0], "direction": 0,
                      "old_position": [0, 0]}


    def check_mouse(self):


        self._attr["old_position"] = self._attr["position"].copy()  # create a copy of the actual position

        if self._attr["mouse"][0] >= self.rect.size[0] - 1:

            self._move(vx=-self._attr["speed"])

        elif self._attr["mouse"][0] <= 1:

            self._move(vx=self._attr["speed"])

        elif self._attr["mouse"][1] <= 1:

            self._move(vy=self._attr["speed"])

        elif self._attr["mouse"][1] >= self.rect.size[1] - 1:

            self._move(vy=-self._attr["speed"])


    def _move(self, vx=0, vy=0):

        self._attr["position"][0] += vx * self._attr["tick"]
        self._attr["position"][1] += vy * self._attr["tick"]

    def up2date(self):

        self._check_borders()
        self.rect = pg.Rect((self._attr["position"][0], self._attr["position"][1]), self.rect.size)

    def set_attr(self, key, value):

        self._attr[key] = value

    def get_attr(self, variable):

        return self._attr[variable]

    def _check_borders(self):

        size_image = self.image.get_size()

        if (-self._attr["position"][0] + self.screen_size[0]) >= size_image[0]:

            self._attr["position"][0] = self.screen_size[0] - size_image[0]

        if (-self._attr["position"][0]) <= 0:

            self._attr["position"][0] = 0

        if (-self._attr["position"][1] + self.screen_size[1]) >= size_image[1]:

            self._attr["position"][1] = self.screen_size[1] - size_image[1]

        if (-self._attr["position"][1]) <= 0:

            self._attr["position"][1] = 0





