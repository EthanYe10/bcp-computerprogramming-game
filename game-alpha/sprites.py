import pygame as pg
import settings

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(settings.WHITE)  # Green color for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        #Stores which screen of the map its on.
        self.mapX = 0
        self.mapY = 0

    def input(self):
        self.vel = pg.Vector2() #Velocity vector

        #https://www.pygame.org/docs/ref/key.html. Code paraphrased from Cozort.
        keystate = pg.key.get_pressed() #Get currently pressed keys

        if keystate[pg.K_w]: #Check if w is pressed.
            self.vel.y -= settings.PLAYER_SPEED
        if keystate[pg.K_s]: #Check if w is pressed.
            self.vel.y += settings.PLAYER_SPEED
        if keystate[pg.K_d]: #Check if w is pressed.
            self.vel.x += settings.PLAYER_SPEED
        if keystate[pg.K_a]: #Check if w is pressed.
            self.vel.x -= settings.PLAYER_SPEED

        #Slow down diagonal movement.

    def update(self):
        #Move based on self.vel vector based on input
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        print(self.rect.x, self.rect.y)