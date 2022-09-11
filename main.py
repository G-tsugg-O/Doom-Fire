import pygame as pg
from pygame import gfxdraw
import sys
import numpy as np
WINDOWMODE = (800,500)
def blurSurf(surface, amt):
    if amt < 1.0:
        raise ValueError("Arg 'amt' must be greater than 1.0, passed in value is %s"%amt)
    scale = 1.0/float(amt)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = pg.transform.smoothscale(surface, scale_size)
    surf = pg.transform.smoothscale(surf, surf_size)
    return surf



class DoomFire:
    def __init__(self,screen,FIRE_XS,FIRE_YS,FIREPIXELSIZE,FIRECOLORSTEPS,COLORS):
        self.screen = screen
        self.FIRE_XS = FIRE_XS
        self.FIRE_YS = FIRE_YS
        self.FIREPIXELSIZE = FIREPIXELSIZE
        self.FIRECOLORSTEPS = FIRECOLORSTEPS
        self.COLORS = COLORS

        self.pallete = self.get_pallete()
        print(self.pallete)
        self.fire_arr = self.get_fire_arr()
        
    def do_fire(self,wind):
        for x in range(self.FIRE_XS):
            for y in range(1, self.FIRE_YS):
                color_index = self.fire_arr[y][x]
                if color_index:
                    rnd = np.random.randint(0,4)
                    self.fire_arr[y - 1][int(x - rnd + (wind+3)) % self.FIRE_XS-1] = color_index - rnd % 2
                else:
                    self.fire_arr[y - 1][x-1] = 0
    def draw_arr(self):
        for y,row in enumerate(self.fire_arr):
            for x, color_index in enumerate(row):
                if color_index:
                    color = self.pallete[color_index]
                    gfxdraw.box(self.screen,(x * self.FIREPIXELSIZE, y * self.FIREPIXELSIZE, self.FIREPIXELSIZE,self.FIREPIXELSIZE),color)
                else:
                    color_index = len(self.pallete)
    def get_fire_arr(self):
        fire_arr = [[0 for i in range(self.FIRE_XS)] for j in range(self.FIRE_YS)]
        for i in range(self.FIRE_XS):
            fire_arr[self.FIRE_YS - 1][i] = len(self.pallete) - 1
        return fire_arr
    def get_pallete(self):
        pallete = [(0,0,0)]
        for i,color in enumerate(self.COLORS[:-1]):
            c1,c2 = color, self.COLORS[i+1]
            for step in range(self.FIRECOLORSTEPS):
                c = pg.Color(c1).lerp(c2,(step + 0.5) / self.FIRECOLORSTEPS)
                pallete.append(c)
        return pallete
    def draw(self,wind):
        self.do_fire(wind)
        self.draw_arr()
screen = pg.display.set_mode(size=WINDOWMODE)
clock = pg.time.Clock()
#doom fire init is    def __init__(self,screen,FIRE_XS,FIRE_YS,FIREPIXELSIZE,FIRECOLORSTEPS,COLORS):
fire1surf = pg.Surface([WINDOWMODE[0]*2,WINDOWMODE[1]], pg.SRCALPHA, 32)
fire1pal = [(255,0,0),(255,165,0),(230,240,250),(255,255,255)]
FIRE1PIXELSIZE=5
FIRE1RES=4
doom_fire = DoomFire(fire1surf,WINDOWMODE[0]*2 // FIRE1PIXELSIZE,WINDOWMODE[1] // FIRE1PIXELSIZE,FIRE1PIXELSIZE,FIRE1RES,fire1pal)
while True:
    for event in pg.event.get():
        if event.type==pg.QUIT:
            pg.quit()
            quit()
            sys.exit()
    clock.tick(float('inf'))
    pg.display.set_caption(f"FPS:{int(clock.get_fps())}")
    fire1surf.fill((0,0,0))
    mousedif = pg.mouse.get_pos()[0]-(WINDOWMODE[0]/2)
    mousedif = mousedif/WINDOWMODE[0]
    mousedif = mousedif*14
    print(mousedif)
    doom_fire.draw(mousedif//2)
    screen.blit(fire1surf,(0,0))
    pg.display.flip()
