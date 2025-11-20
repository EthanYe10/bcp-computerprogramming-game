import pygame as pg
import settings

vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    """Player class
    Author: Matthew Sheyda
    TODO: short description
    """
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

        #These make sure the actions associated with each key only happen once per press, not autofire while held.
        self.Epressed = False
        self.Rpressed = False
        self.Qpressed = False

    def getHeldItem(self):
        for i, sprite in enumerate(self.inventory): #enumerate items in inventory
            if i == self.currentItem: #check if current item is the held item
                return sprite #If so, return the held item

    def input(self):
        self.vel = pg.Vector2() #Velocity vector

        #https://www.pygame.org/docs/ref/key.html. Code paraphrased from Cozort.
        keystate = pg.key.get_pressed() #Get currently pressed keys

        if keystate[pg.K_w]: #Check if w is pressed. Walk up.
            self.vel.y -= settings.PLAYER_SPEED
        if keystate[pg.K_s]: #Check if s is pressed. Walk down.
            self.vel.y += settings.PLAYER_SPEED
        if keystate[pg.K_d]: #Check if d is pressed. Walk right.
            self.vel.x += settings.PLAYER_SPEED
        if keystate[pg.K_a]: #Check if a is pressed. Walk left.
            self.vel.x -= settings.PLAYER_SPEED

        #Slow down diagonal movement.

        if keystate[pg.K_e] and not self.Epressed: #Pick up nearby item. 
            self.Epressed = True #E is now pressed
            hits = pg.sprite.spritecollide(self, self.game.item_sprites, False) #Returns list of item sprites touching player
            #from https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
            for item in hits:
                if not item in self.inventory: #Avoid items already in inventory
                    self.inventory.add(item) #Add first item found
                    self.currentItem = len(self.inventory) - 1 #Immediatly set current item to the new item
                    break #Prevent picking up several items at once
        
        if not keystate[pg.K_e]:
            self.Epressed = False #If e isnt pressed anymore, set e pressed to false.

        if keystate[pg.K_q] and not self.Qpressed: #Switch to next item in inventory
            self.Qpressed = True #Q is now pressed
            self.currentItem += 1
            if self.currentItem >= len(self.inventory): #If at the amount of items in inventory, loop around to first item.
                self.currentItem = 0

        if not keystate[pg.K_q]:
            self.Qpressed = False #If q isnt pressed anymore, set q pressed to false.

        if keystate[pg.K_r] and not self.Rpressed: #Drop held item
            self.Rpressed = True #R is now pressed
            self.inventory.remove(self.getHeldItem())

            #If player was on the last item of inventory and their is no longer an item at current item, decrement.
            if self.currentItem == len(self.inventory) and not self.currentItem == 0: #if currentItem is 0, it will stay so 
                self.currentItem -= 1

        if not keystate[pg.K_r]:
            self.Rpressed = False #If r isnt pressed anymore, set r pressed to false.
            
    #def screenTransition():

    def update(self):
        #Move based on self.vel vector based on input
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y
        #print(self.rect.x, self.rect.y)
        print("Inventory: Length:", len(self.inventory), "Current:", self.currentItem)
        #print(self.currentItem)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.WINDOW_WIDTH:
            self.rect.right = settings.WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT
        # print(self.rect.x // settings.TILESIZE, self.rect.y // settings.TILESIZE)
        # print(self.inventory)

        if not (self.vel.x == 0 and self.vel.y == 0): #If the player is moving, create a fading rectangle for trail effect.
            fr = FadeRect(self.game, (255,255,255,150), settings.PLAYER_TRAIL_DECAY_RATE, self.rect.x, self.rect.y, settings.PLAYER_SIZE, settings.PLAYER_SIZE)
            self.game.all_sprites.add(fr) #Add to all_sprites group
            self.game.effect_sprites.add(fr) #Add to effect_sprites group
        
#Fading rectangle
class FadeRect(pg.sprite.Sprite):
    """FadeRect class
    Author: Matthew Sheyda
    TODO: short description
    """
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
    """Projectile class
    Author: Matthew Sheyda
    TODO: short description
    """
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
        self.velocity.x = (self.velocity.x/settings.PLAYER_SPEED)*speed
        self.velocity.y = (self.velocity.y/settings.PLAYER_SPEED)*speed

        #Doing it this way preserves the direction of the velocity.
        
class BasicBullet(Projectile):
    def __init__(self, game, playerVelocity, x, y):
        #Construct bullet with parameters of this type of bullet:
        super().__init__(game, playerVelocity, settings.WHITE, 20, 3, x, y, 5)
    
    def update():
        pass

class Item(pg.sprite.Sprite):
    """Item class
    Author: Matthew Sheyda
    TODO: short description
    """
    def __init__(self, game, itemImage, x, y, mapX, mapY, itemType):
        pg.sprite.Sprite.__init__(self)
        self.itemImage = itemImage

        self.clearImage = self.image = pg.Surface((16, 16), pg.SRCALPHA) #pg.SRCALPHA allows transparancy
        self.clearImage.fill(settings.TRANSPARANT)

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
                
        #Determine if the item should be drawn, hide by setting image to clearImage
        if self in self.game.player.inventory:
            #Items in inventory should only be visible when held
            if self.game.player.getHeldItem() == self:
                self.image = self.itemImage
            else: 
                self.image = self.clearImage
        else:
            #Item should be visible if not in inventory
            self.image = self.itemImage

class Wall(pg.sprite.Sprite):
    """
    Wall class
    adapted from class code by Ethan Ye to include wall colors
    """
    def __init__(self, game, x, y, color):
        self.game = game
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(
            self, self.groups
        )  # initialize Wall using Sprite class init function

        # wall properties
        self.image = pg.Surface((settings.TILESIZE, settings.TILESIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE

