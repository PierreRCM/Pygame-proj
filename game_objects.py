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
