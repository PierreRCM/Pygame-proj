import pygame as pg
from pygame.locals import *
import os
import game_objects as go
pg.init()


class Map:

    def __init__(self, player):

        self.image = pg.image.load(os.getcwd() + "\\picture\\map.png").convert()
        self.rect = self.image.get_rect()
        self.players = {player.name: player} # will be set depending on the players who connect to the server
        self.bullets = []
        self.client_player = player
        self.last_bullet_code = 641646  # Keep a trace of last bullet code because the server keep sending
                                         # the same bullet while we don't create another bullet

    def deduce_camera_shift(self, camera):
        """to avoid the motion effect on sprite of the camera, it deduce the shift of it"""
        new_pos_camera = camera.get_attr("position")
        old_pos_camera = camera.get_attr("old_position")

        for player in self.players.values():

            x = new_pos_camera[0] - old_pos_camera[0]
            y = new_pos_camera[1] - old_pos_camera[1]
            player.shift(x, y)

        for bullet in self.bullets:

            x = new_pos_camera[0] - old_pos_camera[0]
            y = new_pos_camera[1] - old_pos_camera[1]
            bullet.shift(x, y)

    def update(self, dt):
        """Call update method for all sprites"""
        self._check_alive()

        for player in self.players.values():

            player.update()

        for bullet in self.bullets:

            bullet.update(dt)

    def check_borders(self, screen_position):
        """Check whether player collide with the borders, if it's True, set border arguments"""
        size_image = self.image.get_size()

            # image = sprite.image.get_size() #  HAVE TO USED TO SHIFT FOR LARGE SPRITE, FOR ACCURATE BORDERS

        if (-screen_position[0] + self.client_player._attr["position"][0]) >= size_image[0]:

            self.client_player.set_attr("border", True)

        elif (self.client_player._attr["position"][0] - screen_position[0]) <= 0:

            self.client_player.set_attr("border", True)

        elif (-screen_position[1] + self.client_player._attr["position"][1]) >= size_image[1]:

            self.client_player.set_attr("border", True)

        elif (self.client_player._attr["position"][1] - screen_position[1]) <= 0:

            self.client_player.set_attr("border", True)

        else:

            self.client_player.set_attr("border", False)

    def render(self, screen, camera_rect):

        screen.blit(self.image, camera_rect)

        for player in self.players.values():

            screen.blit(go.image_data_original[player.image], player.rect)

        for bullet in self.bullets:

            screen.blit(go.image_data_original[bullet.image], bullet.rect)

    def _check_alive(self):
        """Check whether each sprites is alive remove them if it's not the case"""

        for bullet in self.bullets:
            if not bullet.get_attr("alive"):

                self.bullets.remove(bullet)

    def handle_new_data(self, list_sprites):
        """This method add data coming from other clients and add it to our map"""

        try:
            for player_name, player_sprite in list_sprites[0].items():

                self.players[player_name] = player_sprite

            if not self._check_code_bullet(list_sprites[1]) and (list_sprites[1].code != self.last_bullet_code):

                self.bullets.append(list_sprites[1])
                self.last_bullet_code = list_sprites[1].code
                print(list_sprites[1].get_attr("position"))

        except IndexError or AttributeError:
            pass

    def _check_code_bullet(self, bullet_sent):

        for bullet in self.bullets:
            if (bullet.code == bullet_sent.code):

                return True
        return False
    def create_data(self):
        """input player instance check whether the player create a sprite,
            It return a dictionary of sprite with the new one"""

        new_sprites = {"Bullet": None, "Player": self.client_player}  # Can only contain the sprite which can be create in the game

        if self.client_player.fire and self.client_player.shot_ready:

            a_bullet = self.client_player.create_bullet()
            self.bullets.append(a_bullet)
            new_sprites["Bullet"] = a_bullet
            self.client_player.fire = False

        return new_sprites

    # def collision(self):
    #     """Test whether each players collide with bullets, deduce hp and kill sprite in case"""
    #
    #     for player in self.groupe_dict["Players"]:
    #         for bullet in self.groupe_dict["Bullets"]:
    #             if (player.name is not bullet.owner) and (player.rect.colliderect(bullet)):
    #
    #                 new_hp = player.get_attr("hp") - bullet.get_attr("damage")
    #                 player.set_attr("hp", new_hp)
    #                 bullet.set_attr("alive", False)


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
        go.init_image("Player", "player.png")  # Todo: change the location of the function init_image()
        go.init_image("Bullet", "bdf.png")

    def check_input(self, inputs):

        if inputs[self.shortcut["FULLSCREEN"]]:

            if not self.fullscreen:

                pg.display.set_mode((self.resolution), pg.FULLSCREEN)

            else:

                pg.display.set_mode(self.resolution)

        if inputs[self.shortcut["QUIT"]]:

            self.window = False
