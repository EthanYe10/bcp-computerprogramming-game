import pygame as pg
import settings
import utils
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    def new(self): #Create a new game and sprites.
        #Create sprite groups
        self.all_sprites = pg.sprite.Group() #Sprite group which contains all sprites

        self.all_inputSprites = pg.sprite.Group() #Sprite group which contains all sprites with input() from the player

        #Instantiate Player, add to sprite groups.
        p = Player(self, 200, 200)
        self.all_inputSprites.add(p)
        self.all_sprites.add(p)

        self.deltaTime = 0
        g.clock = pg.time.Clock()
    def input(self):
        for sprite in self.all_inputSprites:
            sprite.input()
        pass
    def update(self):
        for sprite in self.all_sprites:
            sprite.update()
    def draw(self):
        self.screen.fill(settings.BLUE)
        self.all_sprites.draw(self.screen)
        pg.display.flip()

g = Game()
g.new()

while not pg.event.peek(pg.QUIT): #Checks if there is a quit event in events (User wants to exit).
    g.deltaTime = g.clock.tick(settings.FPS) / 1000

    g.input()
    g.update()
    g.draw()