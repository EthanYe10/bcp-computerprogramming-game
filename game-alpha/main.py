import pygame as pg
import settings
import utils

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))