import pygame as pg

pg.init()
clock = pg.time.Clock()
a = pg.display.set_mode((200, 200), pg.FULLSCREEN)
c = 1
print(pg.display.get_wm_info())
while c :

    b = pg.key.get_pressed()

    if b[pg.K_ESCAPE]:
        pg.display.set_mode((200, 200), pg.FULLSCREEN)
    if b[pg.K_d]:
        pg.display.set_mode((200, 200))

    pg.event.pump()
    clock.tick(10)