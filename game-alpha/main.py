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

        self.input_sprites = pg.sprite.Group() #Sprite group which contains all sprites with input() from the user

        self.item_sprites = pg.sprite.Group() #Sprite group for items 

        self.effect_sprites = pg.sprite.Group() #Sprite group for visual effects related sprites

        #Instantiate Player, add to sprite groups.
        self.player = Player(self, 200, 200) #Store player reference for later access
        self.input_sprites.add(self.player)
        self.all_sprites.add(self.player)

        #Create delta time and pg.Clock attributes.
        self.deltaTime = 0
        g.clock = pg.time.Clock()

        #Create item classes
        img = pg.image.load("images\\blackKey.png").convert_alpha()
        itm = Item(self, img, 200, 200, 0, 0, settings.ITEM_TYPE_KEY_BLACK)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)
    def input(self):
        #Loop through all sprites that take input and scan for input.
        for sprite in self.input_sprites:
            sprite.input()
        pass
    def update(self):
        #run update function of all sprites
        for sprite in self.all_sprites:
            sprite.update()
    def draw(self):
        self.screen.fill(settings.BLUE)
        #Draw sprites in specific order to prevent layering issues.
        self.effect_sprites.draw(self.screen)
        self.input_sprites.draw(self.screen)
        self.item_sprites.draw(self.screen)
        pg.display.flip()

g = Game()
g.new()

while not pg.event.peek(pg.QUIT): #Checks if there is a quit event in events (User wants to exit).
    g.deltaTime = g.clock.tick(settings.FPS) / 1000

    g.input()
    g.update()
    g.draw()