import pygame as pg
import settings

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((settings.PLAYER_SIZE, settings.PLAYER_SIZE))
        self.image.fill(settings.WHITE)  # Green color for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.game = game

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

    #def screenTransition():

    def update(self):
        #Move based on self.vel vector based on input
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        print(self.rect.x, self.rect.y)

        if not (self.vel.x == 0 and self.vel.y == 0): #If the player is moving, create a fading rectangle for trail effect.
            fr = FadeRect(self.game, (255,255,255,150), settings.PLAYER_TRAIL_DECAY_RATE, self.rect.x, self.rect.y, settings.PLAYER_SIZE, settings.PLAYER_SIZE)
            self.game.all_sprites.add(fr) #Add to all_sprites group
            self.game.effect_sprites.add(fr) #Add to effect_sprites group
        
#Fading rectangle
class FadeRect(pg.sprite.Sprite):
    def __init__(self, game, color, decayRate, xLocation, yLocation, xSize, ySize):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((xSize, ySize), pg.SRCALPHA) #pg.SRCALPHA allows there to be an alpha channel in the image
        self.image.fill(color)  #Color of the rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (xLocation, yLocation)

        self.decayRate = decayRate
    
    def update(self):
        if not self.image.get_alpha() < self.decayRate: #If the current alpha of the image is not lower than the decay rate
            self.image.set_alpha(self.image.get_alpha()-self.decayRate) #Fade out by set decayRate
        else:
            self.kill() #kill self once faded.