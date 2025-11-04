import pygame as pg

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill((0, 255, 0))  # Green color for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
    