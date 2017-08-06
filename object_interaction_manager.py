import pygame as pg
import game_objects as go
import numpy as np

def update_sprite(groupe_sprite, screen, camera, oldrect):

    new_pos_camera = camera.get_attr("position")
    old_pos_camera = camera.get_attr("old_position")

    for sprite in groupe_sprite.sprites():

        x = new_pos_camera[0] - old_pos_camera[0]
        y = new_pos_camera[1] - old_pos_camera[1]

        sprite.shift(x, y)
        sprite.up2date()

        screen.blit(sprite.image, sprite.rect)

    return oldrect + [sprite.rect for sprite in groupe_sprite.sprites()] # return list of old rect and new rect to update

def cooldown(spell_to_cast, groupe, spells_list):
    """Check if the spell is ready, and return the group with or without the spell"""

    now = pg.time.get_ticks()

    if (now - spells_list[spell_to_cast.get_attr("name")])/1000 >= spell_to_cast.get_attr("cooldown"):

        groupe.add(spell_to_cast)
        spells_list[spell_to_cast.get_attr("name")] = pg.time.get_ticks()

    return groupe

def check_alive(groupe):

    for sprite in groupe:
        if not sprite.get_attr("alive"):
            groupe.remove(sprite)

    return groupe

