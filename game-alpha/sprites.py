import pygame as pg
import settings

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((settings.PLAYER_SIZE, settings.PLAYER_SIZE))
        self.image.fill(settings.WHITE)  #White color for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.game = game

        #Stores which screen of the map its on.
        self.mapX = 0
        self.mapY = 0

        self.inventory = pg.sprite.Group() #Inintialize inventory (a sprite group of item sprites)
        self.currentItem = 0 #Set current item to 0.

    def input(self):
        self.vel = pg.Vector2() #Velocity vector

        #https://www.pygame.org/docs/ref/key.html. Code paraphrased from Cozort.
        keystate = pg.key.get_pressed() #Get currently pressed keys

        if keystate[pg.K_w]: #Check if w is pressed.
            self.vel.y -= settings.PLAYER_SPEED
        if keystate[pg.K_s]: #Check if s is pressed.
            self.vel.y += settings.PLAYER_SPEED
        if keystate[pg.K_d]: #Check if d is pressed.
            self.vel.x += settings.PLAYER_SPEED
        if keystate[pg.K_a]: #Check if a is pressed.
            self.vel.x -= settings.PLAYER_SPEED

        #Slow down diagonal movement.

        if keystate[pg.K_e]: #Pick up nearby item
            hits = pg.sprite.spritecollide(self, self.game.item_sprites, False) #Returns list of item sprites touching player
            #from https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
            if len(hits) > 0: #Check the length of the list to prevent index out of range error
                self.inventory.add(hits[0]) #Adds the first item returned into the inventory.

        if keystate[pg.K_q]: #Switch to next item in inventory
            self.currentItem += 1
            if self.currentItem == len(self.inventory): #If at the amount of items in inventory, loop around to first item.
                self.currentItem = 0

        if keystate[pg.K_r]: #Drop held item
            for i, sprite in enumerate(self.inventory):
                if i == self.currentItem: #Find current item in inventory
                    self.inventory.remove(sprite) #Remove the item from inventory
            
    #def screenTransition():

    def update(self):
        #Move based on self.vel vector based on input
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        print(self.rect.x, self.rect.y)
        print(self.inventory)
        print(self.currentItem)

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

        self.decayRate = decayRate #amount by which alpha is of the rectangle decreased, per frame
    
    def update(self):
        if not self.image.get_alpha() < self.decayRate: #If the current alpha of the image is not lower than the decay rate
            self.image.set_alpha(self.image.get_alpha()-self.decayRate) #Fade out by set decayRate
        else:
            self.kill() #kill self once faded.

class Projectile(pg.sprite.Sprite):
    def __init__(self, game, playerVelocity, color, speed, countdownSeconds, xLocation, yLocation, size):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((size, size))
        self.image.fill(color)  #Color of the rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (xLocation, yLocation)

        self.game = game #Reference to the game to detect collidable entities

        #Create bullet's vector
        self.velocity = playerVelocity #Set to playerVelocity

        #Divide by PLAYER_SPEED (to make all members 1), multiply by speed to get bullet velocity.
        self.velocity.x = (self.velocity.x/PLAYER_SPEED)*speed
        self.velocity.y = (self.velocity.y/PLAYER_SPEED)*speed

        #Doing it this way preserves the direction of the velocity.
        
class BasicBullet(Projectile):
    def __init__(self, game, playerVelocity, x, y):
        #Construct bullet with parameters of this type of bullet:
        super().__init__(game, playerVelocity, WHITE, 20, 3, x, y, 5)
    
    def update():
        pass

class Item(pg.sprite.Sprite):
    def __init__(self, game, itemImage, x, y, mapX, mapY, itemType):
        pg.sprite.Sprite.__init__(self)
        self.image = itemImage #Image representing the item
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.mapX = mapX
        self.mapY = mapY
        
        self.itemType = itemType
        self.game = game

    def update(self):
        #If in player's inventory, go to player's location.
        if self in self.game.player.inventory:
            self.rect.topleft = (self.game.player.rect.x,self.game.player.rect.y)
