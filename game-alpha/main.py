import pygame as pg
import settings
import utils

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
    def update(self):
        pass
    def new(self): #Create a new game and sprites.
        self.p = Player(self, 6, 7)

g = Game()

while not pg.event.peek(pg.QUIT): #Checks if there is a quit event in events (User wants to exit).
    g.update()