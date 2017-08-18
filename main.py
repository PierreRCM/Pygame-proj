
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
        self.map = wm.Map({"Players": pg.sprite.Group(self.player), "Bullets": pg.sprite.Group()})
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
            self.player.check_inputs()  # todo: Try to find a way to avoid moving and rotation the player in this method

            self.input = pg.key.get_pressed()

            self.camera.set_attr("tick", self.dt)
            self.camera.check_mouse()
            self.camera.update()

            dict_new_sprites = self.map.add_sprites(self.player)  # Need player instance to check whether the player is shooting
            data = self._create_data(dict_new_sprites)

            # Updating / displaying on screen
            self.map.deduce_camera_shift(self.camera)
            self.map.check_borders(self.camera.get_attr("position"))
            self.map.collision()
            self.map.update()
            self.map.render(self.screen.screen, self.camera.rect)

            self.screen.check_input(self.input)

            self.client.send(data)

            pg.display.update()
            pg.event.pump()
            self.gameOn = self.screen.window

    def _create_data(self, dict_new_sprites):

        dict = {}

        if self.player.fire:

            dict["Bullet"] = dict_new_sprites["Bullet"]

        if self.player.move:

            dict["Player"] = dict_new_sprites["Player"]

        return dict


main = Main()
main.game_loop()

import pygame as pg
import os
from pygame.locals import *
import window_manager as wm
import game_objects as go
import object_interaction_manager as oim
import files_manager as fm
# we can imagine that each short cut key have a string corresping to the action he want to do, so in action you may change those bind
pg.init()
pg.display.init()
print(pg.display.Info())
size_window = (800, 600)
screen = pg.display.set_mode(size_window)
clock = pg.time.Clock()
gameOn = True
pg.key.set_repeat(10, 10)

player = go.Player()
groupe_actif = pg.sprite.Group(player)
groupe_list = [groupe_actif.copy()]
map = wm.Map(groupe_list, groupe_actif)
camera = wm.Camera(size_window, map.image.get_size())

map.render(screen, camera.rect)
pg.display.update()

while gameOn:

    dt = clock.tick(50) / 1000

    player.set_attr("tick", dt)
    camera.set_attr("tick", dt)

    for event in pg.event.get():

        if event.type == QUIT:

            gameOn = False

        if event.type == MOUSEMOTION:

            player.set_attr("mouse", list(pg.mouse.get_pos()))
            camera.set_attr("mouse", list(pg.mouse.get_pos()))

        if event.type == KEYDOWN:

            # if event.key == K_F1:
            #     wm.screen = pg.display.set_mode(wm.size_window, FULLSCREEN)
            #     pg.display.update()

            if event.key == player.get_attr("UP"):

                player.move(vy=-player.get_attr("speed"))

            if event.key == player.get_attr("DOWN"):

                player.move(vy=player.get_attr("speed"))

            if event.key == player.get_attr("LEFT"):

                player.move(vx=-player.get_attr("speed"))

            if event.key == player.get_attr("RIGHT"):

                player.move(vx=player.get_attr("speed"))

            # if event.key == player.get_attr("R1"):
            #
            #     spell = go.Spell(name = "fireball", direction = player.get_attr("direction"), position = player.get_attr("position").copy(),
            #                      tick = player.get_attr("tick"))
            #
            #     groupe_actif = oim.cooldown(spell, map.groupe_actif, fm.spells_time)

    ###################################################################
                        # manage objects then update
    ###################################################################


    camera.check_mouse()
    camera.update()

    map.deduce_camera_shift(camera)
    map.check_borders(camera.get_attr("position"), size_window)
    map.update()
    # oldrect = [sprite.rect for sprite in groupe.sprites()]
    # groupe = oim.check_alive(groupe)
    map.render(screen, camera.rect) # display background

    # rect_list = oim.update_sprite(groupe, wm.screen, camera, oldrect)# if a sprite died no rect return for this sprite

    pg.display.update()
    # if camera.get_attr("speed") is not 0:
    #     pg.display.update()
    # else:
    #     pg.display.update(rect_list)



