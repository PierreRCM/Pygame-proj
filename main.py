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


timer = pg.time.Clock()
clock = pg.time.Clock()
gameOn = True
pg.key.set_repeat(10, 10)


camera = wm.Camera(wm.size_window, wm.background)
player = go.Player()
groupe = pg.sprite.Group(player)

wm.screen.blit(camera.image, camera.rect)
pg.display.update()

while gameOn:

    dt = timer.tick() / 1000
    player.set_attr("tick", dt)
    camera.set_attr("tick", dt)

    for event in pg.event.get():

        if event.type == QUIT:

            gameOn = False

        if event.type == MOUSEMOTION:

            player.set_attr("mouse", list(pg.mouse.get_pos()))
            camera.set_attr("mouse", list(pg.mouse.get_pos()))

        if event.type == KEYDOWN:

            if event.key == K_F1:
                wm.screen = pg.display.set_mode(wm.size_window, FULLSCREEN)
                pg.display.update()

            if event.key == player.get_attr("UP"):

                player.move(vy=-player.get_attr("speed"))

            if event.key == player.get_attr("DOWN"):

                player.move(vy=player.get_attr("speed"))

            if event.key == player.get_attr("LEFT"):

                player.move(vx=-player.get_attr("speed"))

            if event.key == player.get_attr("RIGHT"):

                player.move(vx=player.get_attr("speed"))

            if event.key == player.get_attr("R1"):

                spell = go.Spell(name = "fireball", direction = player.get_attr("direction"), position = player.get_attr("position").copy(),
                                 tick = player.get_attr("tick"))

                groupe = oim.cooldown(spell, groupe, fm.spells_time)

    ###################################################################
                        # manage objects then update
    ###################################################################


    camera.check_mouse()
    camera.up2date()

    oldrect = [sprite.rect for sprite in groupe.sprites()]
    groupe = oim.check_alive(groupe)
    wm.screen.blit(camera.image, camera.rect) # display background

    rect_list = oim.update_sprite(groupe, wm.screen, camera, oldrect)# if a sprite died no rect return for this sprite

    if camera.get_attr("speed") is not 0:
        pg.display.update()
    else:
        pg.display.update(rect_list)


    clock.tick(50)
