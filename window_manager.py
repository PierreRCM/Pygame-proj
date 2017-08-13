import pygame as pg
from pygame.locals import *
import os
import game_objects as go
pg.init()


class Map:

    def __init__(self, groupe_dict):

        self.image = pg.image.load(os.getcwd() + "\\picture\\map.png").convert()
        self.rect = self.image.get_rect()
        self.groupe_dict = groupe_dict # contain group actif (who need to be update) and static sprites group


    def deduce_camera_shift(self, camera):

        new_pos_camera = camera.get_attr("position")
        old_pos_camera = camera.get_attr("old_position")

        for groupe in self.groupe_dict.values():

            for sprite in groupe.sprites():

                x = new_pos_camera[0] - old_pos_camera[0]
                y = new_pos_camera[1] - old_pos_camera[1]

                sprite.shift(x, y)

    def update(self):

        self._check_alive()

        for groupe in self.groupe_dict.values():

            groupe.update()

    def check_borders(self, screen_position):

        size_image = self.image.get_size()

        for sprite in self.groupe_dict["a"].sprites():

            # image = sprite.image.get_size() #  HAVE TO USED TO SHIFT FOR LARGE SPRITE, FOR ACCURATE BORDERS

            if (-screen_position[0] + sprite._attr["position"][0]) >= size_image[0]:

                sprite.set_attr("border", True)

            elif (sprite._attr["position"][0] - screen_position[0]) <= 0:

                sprite.set_attr("border", True)

            elif (-screen_position[1] + sprite._attr["position"][1]) >= size_image[1]:

                sprite.set_attr("border", True)

            elif (sprite._attr["position"][1] - screen_position[1]) <= 0:

                sprite.set_attr("border", True)

            else:

                sprite.set_attr("border", False)

    def render(self, screen, camera_rect):

        screen.blit(self.image, camera_rect)

        for groupe in self.groupe_dict.values():

            for sprite in groupe.sprites():

                screen.blit(go.image_data_original[sprite.image], sprite.rect)

    def add_sprites(self, player):

        if player.fire and player.shot_ready:

            self.groupe_dict["a"].add(player.create_bullet())

    def _check_alive(self):

        for sprite in self.groupe_dict["a"].sprites():

            if not sprite.get_attr("alive"):

                self.groupe_dict["a"].remove(sprite)


class Camera:

    def __init__(self, screen_size, map_size):

        self.map_size = map_size
        self.screen_size = screen_size
        self.rect = pg.Rect((0, 0) , screen_size)
        self._attr = {"mouse": [0, 0], "speed": 100, "tick": 0, "position": [0, 0], "direction": 0,
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

    def update(self):

        self._check_borders()
        self.rect = pg.Rect((self._attr["position"][0], self._attr["position"][1]), self.rect.size)

    def set_attr(self, key, value):

        self._attr[key] = value

    def get_attr(self, variable):

        return self._attr[variable]

    def _check_borders(self):


        if (-self._attr["position"][0] + self.screen_size[0]) >= self.map_size[0]:

            self._attr["position"][0] = self.screen_size[0] - self.map_size[0]

        if (-self._attr["position"][0]) <= 0:

            self._attr["position"][0] = 0

        if (-self._attr["position"][1] + self.screen_size[1]) >= self.map_size[1]:

            self._attr["position"][1] = self.screen_size[1] - self.map_size[1]

        if (-self._attr["position"][1]) <= 0:

            self._attr["position"][1] = 0


class Screen:

    def __init__(self):

        self.resolution = (500, 500)
        self.screen = pg.display.set_mode(self.resolution)
        self.fullscreen = False
        self.game_name = pg.display.set_caption("ACTUALLY NONE")
        self.shortcut = {"FULLSCREEN": K_F1, "QUIT": K_ESCAPE} # we may create a menu when pressing a key
                                                               # so we can access to option/exit
                                                               # and handle it with mouse click
        self.window = True

    def check_input(self, inputs):

        if inputs[self.shortcut["FULLSCREEN"]]:

            if not self.fullscreen:

                pg.display.set_mode((self.resolution), pg.FULLSCREEN)

            else:

                pg.display.set_mode(self.resolution)

        if inputs[self.shortcut["QUIT"]]:

            self.window = False
