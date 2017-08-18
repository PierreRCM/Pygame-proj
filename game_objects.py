 socket-first-step
import numpy as np
import os
import pygame as pg
from pygame.locals import *
import pandas as pd
# Todo: Rework on weapon_data, maybe the server can initialize random position for weapon in the map and you have to
# Todo picked it up so the server got the data of the weapons.
pg.init()
weapon_data = pd.DataFrame(index=["speed", "range", "damage", "accuracy", "reloading_time", "loader", "rate"],
                           columns=["Gun"])
weapon_data["Gun"]["speed"] = 400
weapon_data["Gun"]["range"] = 200
weapon_data["Gun"]["damage"] = 10
weapon_data["Gun"]["accuracy"] = 10
weapon_data["Gun"]["reloading_time"] = 1
weapon_data["Gun"]["loader"] = 10
weapon_data["Gun"]["rate"] = 0.2

image_data_original = {"Player": None, "Bullet": None}

image_data = {"Player": None, "Bullet": None}


class Bullet(pg.sprite.Sprite):

    def __init__(self, name, direction, position, range_, damage, speed, tick):

        self.owner = name  # Used for collision
        self.image = "Bullet"
        self._init_image()
        image_data[self.image].set_colorkey((255, 255, 255))
        image_data_original[self.image].set_colorkey((255, 255, 255))
        self.rect = pg.Rect((position[0], position[1]), image_data_original[self.image].get_size())
        # Depend on the weapon characteristics
        self._attr = {"direction": direction - 90, "reference": 270, "init_position": position.copy(),
                      "position": position.copy(), "distance_traveled": 0, "speed": speed,
                      "damage": damage, "tick": tick,  # todo: set real tick time of the loop
                      "range": range_, "alive": True, "border": False}

        self._rotate()

        pg.sprite.Sprite.__init__(self)

    def get_attr(self, variable):
        """input string variable,
           find in dictionnary self._attr argument required
           output depend of variable asked"""
        return self._attr[variable]

    def _move(self):
        """move the spell, shift 90° because 0 stand for 90 """
        self._attr["position"][0] += np.cos((self._attr["direction"] + 90) * np.pi / 180) * self._attr["speed"] * self._attr["tick"]
        self._attr["position"][1] += np.sin(-(self._attr["direction"] + 90) * np.pi / 180) * self._attr["speed"] * self._attr["tick"]

        self._attr["distance_traveled"] += self._attr["speed"] * self._attr["tick"]
        # get distance travelled by the sprite so we can remove when it's superior to the range of the spell

    def update(self):
        """First we move the spell then the rectangle"""

        self._move()
        self.rect = pg.Rect((self._attr["position"][0], self._attr["position"][1]),
                            image_data_original[self.image].get_size())
        self._outrange()
        self._outborder()

    def _rotate(self):
        """input newdirection in degree
           rotate the image in subtracting by the reference (position of picture)"""
        image_data[self.image] = pg.transform.rotate(image_data_original[self.image],
                                                     (self._attr["direction"] - self._attr["reference"]))
        self._attr["reference"] = self._attr["direction"]

    def _outrange(self):

        if self._attr["distance_traveled"] >= self._attr["range"]:

            self._attr["alive"] = False

    def shift(self, x, y):

        self._attr["position"][0] += x
        self._attr["position"][1] += y

    def _outborder(self):

        if self._attr["border"]:

            self._attr["alive"] = False

    def set_attr(self, key, value):

        self._attr[key] = value

    def _init_image(self):
        global image_data_original, image_data

        image_data_original[self.image] = pg.image.load(os.getcwd() + "\\picture\\bdf.png").convert()
        image_data[self.image] = pg.image.load(os.getcwd() + "\\picture\\bdf.png").convert()


class Weapon:

    def __init__(self, name):

        self.name = name
        self.rate = self._set_stat("rate")
        self.range = self._set_stat("range")
        self.damage = self._set_stat("damage")
        self.speed = self._set_stat("speed")
        self.accuracy = self._set_stat("accuracy")
        self.reloading_time = self._set_stat("reloading_time")
        self.loader = self._set_stat("loader")

    def _set_stat(self, key):

        global weapon_data

        return weapon_data[self.name][key]


class Player(pg.sprite.Sprite):

    def __init__(self):

        self.name = "Player1"
        self.image = "Player"  # image that ll be blit
        self._init_image()
        image_data_original[self.image].set_colorkey((255, 255, 255))  # Set image transparence
        self.rect = image_data_original[self.image].get_rect()  # called when updating sprite
        self.weapon = Weapon("Gun")
        self.shortcut = {"up": K_w, "down": K_s, "left": K_a, "right": K_d, "shoot": K_1}
        self.last_shot = pg.time.get_ticks()
        self._attr = {"reference": 270, "position": [25, 25], "old_position": [10, 10], "speed": 40, "hp": 100,
                      "alive": True, "border": False, "mouse": [0, 0], "direction": 0, "tick": 0}
        self.shot_ready = True
        self.fire = False
        self.move = False

        self.keys = pg.key.get_pressed()
        pg.sprite.Sprite.__init__(self)

    def _move(self, vx=0, vy=0):
        """input time between last call of clock.tick()
           compute the distance in pixel/second"""
        if vx != 0 and vy != 0:

            vx = np.cos(np.pi/4)*vx
            vy = np.cos(np.pi/4)*vy

        if not self._attr["border"]:

            self._attr["old_position"] = self._attr["position"].copy()
            self._attr["position"][0] += (vx*self._attr["tick"])
            self._attr["position"][1] += (vy*self._attr["tick"])

        else:

            self._attr["position"] = self._attr["old_position"].copy()

    def get_attr(self, variable):
        """input string variable,
           find in dictionary self._attr argument required
           output depend of variable asked"""

        return self._attr[variable]

    def _rotate(self):
        """Rotate the image in calculating the the angle, between mouse position and player position"""

        old_direction = self._attr["direction"]
        deltax = self._attr["mouse"][0] - self._attr["position"][0]
        deltay = self._attr["mouse"][1] - self._attr["position"][1]
        # difference of position between position of sprite and mouse position
        self._attr["direction"] = np.arctan2(deltax, deltay) * 180 / np.pi + self._attr["reference"]

        # difference of angle between the old and new position
        if old_direction - self._attr["direction"]:

            image_data[self.image] = pg.transform.rotate(image_data_original[self.image], self._attr["direction"])
            self.move = True

        else:

            self.move = False

    def set_attr(self, variable, value):

        self._attr[variable] = value

    def update(self):
        """Update new rectangle"""

        self._rotate()
        center_image = image_data_original[self.image].get_rect().center  # center of our rotated image,
        self.rect = pg.Rect((self._attr["position"][0] - center_image[0],  # so we can position our rectangle
                             self._attr["position"][1] - center_image[1]), image_data_original[self.image].get_size())

    def shift(self, x, y):

        self._attr["position"][0] += x
        self._attr["position"][1] += y
        self._attr["old_position"][0] += x
        self._attr["old_position"][1] += y

    def _cooldown_shot(self):
        """ Check difference between now and last shot, depend on the weapon's rate """

        now = pg.time.get_ticks()

        if (now - self.last_shot)/1000 >= self.weapon.rate:

            self.last_shot = now

            self.shot_ready = True

        else:

            self.shot_ready = False

    def create_bullet(self):
        """return a bullet instance"""

        new_bullet = Bullet(self.name, self._attr["direction"], self._attr["position"], self.weapon.range,
                            self.weapon.damage, self.weapon.speed, self._attr["tick"])  # get_attr method for weapon
        self.fire = False

        return new_bullet

    def check_inputs(self):

        self.move = False

        vx = 0
        vy = 0

        if self.keys[self.shortcut["up"]]:

            self.move = True
            vy = -self._attr["speed"]

        elif self.keys[self.shortcut["down"]]:

            self.move = True
            vy = self._attr["speed"]

        if self.keys[self.shortcut["left"]]:

            self.move = True
            vx = -self._attr["speed"]

        elif self.keys[self.shortcut["right"]]:

            self.move = True
            vx = self._attr["speed"]

        if self.keys[self.shortcut["shoot"]]:

            self.fire = True
            self._cooldown_shot()

        self._move(vx=vx, vy=vy)


    def _init_image(self):

        global image_data_original, image_data

        image_data_original[self.image] = pg.image.load(os.getcwd() + "\\picture\\player.png").convert()
        image_data[self.image] = pg.image.load(os.getcwd() + "\\picture\\player.png").convert()

import numpy as np
import os
import pygame as pg
from pygame.locals import *

background_size = pg.image.load(os.getcwd() + "\\picture\\map.jpg").get_size()
size_window = (800, 600)

class Spell(pg.sprite.Sprite):

    def __init__(self, direction, position , tick, name):
        # In the futur set all attributs in function of the name of the spell enter, if i enter frostbolt,retrieve data
        # or maybe a dictionnary define out of the class containing all the spell of the game
        # for the moment attribut (in the dictionary) are sets randomly, even more for the "last call"
        # we have to store the last time we use that type of spell so we can manage the spell we can cast
        """ input position of the caster, the old direction is set to 270 because of the sprite direction"""
        self.image = pg.image.load(os.getcwd() + "\\picture\\bdf.png").convert()
        self.image.set_colorkey((255, 255, 255))
        self.rect = pg.Rect((position[0], position[1]), self.image.get_size())
        self._attr = {"name": name, "direction": direction-90, "reference": 270, "init_position": position.copy(),
                      "position": position, "distance_traveled": 0, "speed": 500, "damage": 30, "tick": tick,
                      "cooldown": 0.5, "range": 500, "alive": True, "border": False}
        pg.sprite.Sprite.__init__(self)

    def get_attr(self, variable):
        """input string variable,
           find in dictionnary self._attr argument required
           output depend of variable asked"""
        return self._attr[variable]

    def _move(self):
        """move the spell, shift 90° because 0 stand for 90 """

        self._attr["position"][0] += np.cos((self._attr["direction"] + 90)* np.pi / 180) * self._attr["speed"] * self._attr["tick"]
        self._attr["position"][1] += np.sin(-(self._attr["direction"] + 90)* np.pi / 180) * self._attr["speed"] * self._attr["tick"]

        self._attr["distance_traveled"] = np.sqrt((self._attr["position"][0] - self._attr["init_position"][0])**2 +
                                                  (self._attr["position"][1] - self._attr["init_position"][1]) ** 2)
        # get distance travelled by the sprite so we can remove when it's superior to the range of the spell
    def update(self):
        """First we move the spell then the rectangle"""

        self._rotate()
        self._move()
        self.rect = pg.Rect((self._attr["position"][0], self._attr["position"][1]), self.image.get_size())
        self._outrange()
        self._outborder()

    def _rotate(self):
        """input newdirection in degree
           rotate the image in subtracting by the reference (position of picture)"""
        self.image = pg.transform.rotate(self.image, (self._attr["direction"] - self._attr["reference"]))
        self._attr["reference"] = self._attr["direction"]

    def _outrange(self):

        if self._attr["distance_traveled"] >= self._attr["range"]:

            self._attr["alive"] = False

    def shift(self, x, y):

        self._attr["position"][0] += x
        self._attr["position"][1] += y

    def _outborder(self):

        if self._attr["border"]:

            self._attr["alive"] = False


class Player(pg.sprite.Sprite):


    def __init__(self):

        self.original = pg.image.load(os.getcwd() + "\\picture\\Player.png").convert() # image of reference for rotation
        self.image = self.original.copy() # image that ll be blit
        self.original.set_colorkey((255, 255, 255)) # Set image transparence
        self.rect = self.image.get_rect() # called when updating sprite

        self._attr = {"reference": 270, "position": [25, 25],"old_position":[10, 10], "speed": 150, "hp": 100, "mana": 100,
                      "alive": True, "border": False, "mouse": [0, 0], "direction": 0, "tick": 0,
                      "UP": K_w, "DOWN": K_s, "LEFT": K_a, "RIGHT": K_d, "R1": K_1}
        pg.sprite.Sprite.__init__(self)

    def move(self, vx=0, vy=0):
        """input time between last call of clock.tick()
           compute the distance in pixel/second"""

        if not self._attr["border"]:

            self._attr["old_position"] = self._attr["position"].copy()
            self._attr["position"][0] += (vx*self._attr["tick"])
            self._attr["position"][1] += (vy*self._attr["tick"])

        else:
            self._attr["position"] = self._attr["old_position"].copy()

    def get_attr(self, variable):
        """input string variable,
           find in dictionary self._attr argument required
           output depend of variable asked"""
        return self._attr[variable]

    def _rotate(self):
        """ rotate the image in subtracting by the old direction direction - reference"""

        deltaX = self._attr["mouse"][0] - self._attr["position"][0]
        deltaY = self._attr["mouse"][1] - self._attr["position"][1]
        # difference of position between position of sprite and mouse position
        self._attr["direction"] = np.arctan2(deltaX, deltaY) * 180 / np.pi + self._attr["reference"]
        # difference of angle between the old and new position
        self.image = pg.transform.rotate(self.original, self._attr["direction"])

    def set_attr(self, variable, value):

        self._attr[variable] = value

    def update(self):
        """Update new rectangle"""

        self._rotate()
        center_image = self.image.get_rect().center # center of our rotated image, so we can position our rectangle
        self.rect = pg.Rect((self._attr["position"][0] - center_image[0],
                             self._attr["position"][1] - center_image[1]), self.image.get_size())

    def shift(self, x, y):
        #
        self._attr["position"][0] += x
        self._attr["position"][1] += y
        self._attr["old_position"][0] += x
        self._attr["old_position"][1] += y

