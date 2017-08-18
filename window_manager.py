import pygame as pg
from pygame.locals import *
import os
import game_objects as go
pg.init()


class Map:

    def __init__(self, groupe_dict):

        self.image = pg.image.load(os.getcwd() + "\\picture\\map.png").convert()
        self.rect = self.image.get_rect()
        self.groupe_dict = groupe_dict # Actually contain 2 sprite groupe keys Bullets and Players

    def deduce_camera_shift(self, camera):
        """to avoid the motion effect on sprite of the camera, it deduce the shift of it"""
        new_pos_camera = camera.get_attr("position")
        old_pos_camera = camera.get_attr("old_position")

        for groupe in self.groupe_dict.values():

            for sprite in groupe.sprites():

                x = new_pos_camera[0] - old_pos_camera[0]
                y = new_pos_camera[1] - old_pos_camera[1]

                sprite.shift(x, y)

    def update(self):
        """Call update method for all sprites"""
        self._check_alive()

        for groupe in self.groupe_dict.values():

            groupe.update()

    def check_borders(self, screen_position):
        """Check whether sprites collide with the borders, if it's True, set border arguments"""
        size_image = self.image.get_size()

        for groupe in self.groupe_dict.values():
            for sprite in groupe.sprites():

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
        """input player instance check whether the player create a sprite, add it to the map
            It also return a dictionnary of sprite the new sprite created"""

        new_sprites = {"Bullet": None, "Player": player}  # Can only contain the sprite which can be create in the game

        if player.fire and player.shot_ready:

            a_bullet = player.create_bullet()
            self.groupe_dict["Bullets"].add(a_bullet)
            new_sprites["Bullet"] = a_bullet
            player.fire = False

        return new_sprites

    def _check_alive(self):
        """Check whether each sprites is alive remove them if it's not the case"""

        for groupe in self.groupe_dict.values():
            for sprite in groupe.sprites():
                if not sprite.get_attr("alive"):

                    groupe.remove(sprite)

    def handle_new_data(self, data_from_server):
        """This method add data coming from other clients and add it to our map"""

        for data_dict in data_from_server:  # Most of the time data_from_server contain only 1 list
            for sprite in data_dict.values():        # just to handle latency between packets
                if isinstance(sprite, go.Player):

                    self.groupe_dict["Players"].add(sprite)  # data send are only active sprites

                elif isinstance(sprite, go.Bullet):

                    self.groupe_dict["Bullets"].add(sprite)

    def collision(self):
        """Test whether each players collide with bullets, deduce hp and kill sprite in case"""

        for player in self.groupe_dict["Players"]:
            for bullet in self.groupe_dict["Bullets"]:
                if (player.name is not bullet.owner) and (player.rect.colliderect(bullet)):

                    new_hp = player.get_attr("hp") - bullet.get_attr("damage")
                    player.set_attr("hp", new_hp)
                    bullet.set_attr("alive", False)


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
