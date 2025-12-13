import pygame as pg
import settings
import math
import random
# from main import Game

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

        # slow down diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.70710678118

        if keystate[pg.K_e] and not self.Epressed: #Pick up nearby item. 
            self.Epressed = True #E is now pressed
            hits = pg.sprite.spritecollide(self, self.game.item_sprites, False) #Returns list of item sprites touching player
            #from https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.spritecollide
            for item in hits:
                if not (item in self.inventory) and item.map == self.game.current_map and len(self.inventory) < settings.PLAYER_ITEM_CAPACITY: #Avoid items already in inventory, not in current map (thus hidden), if item capacity is full
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

            if len(self.inventory) > 0: #Prevent crash from if statement getting .map of NoneType.
                self.getHeldItem().map = self.game.current_map #Set item map to the map it is being dropped at.
                self.inventory.remove(self.getHeldItem())

                #If player was on the last item of inventory and their is no longer an item at current item, decrement.
                if self.currentItem == len(self.inventory) and not self.currentItem == 0: #if currentItem is 0, it will stay so 
                    self.currentItem -= 1

        if not keystate[pg.K_r]:
            self.Rpressed = False #If r isnt pressed anymore, set q pressed to false.

        if keystate[pg.K_SPACE]: #Fire weaopn (If has one)
            #Check which weapon is held to determine which bullet to fire.
            item = self.getHeldItem()
            if len(self.inventory) > 0: #Prevent crash from if statement getting .map of NoneType.
                if item.itemType == settings.ITEM_TYPE_WEAPON_TESLA and not (self.vel.x == 0 and self.vel.y == 0): #To make sure there's an itemType attribute. Also make sure player isnt standing still for bullet to fire
                    p = Projectile(self.game, self.vel, settings.WHITE, 20, 2, self.rect.x, self.rect.y, 5)
                    self.game.all_sprites.add(p)
                    self.game.projectile_sprites.add(p)

    def wallCollide_x(self):
        #Code by Ethan Ye paraphrased from cozort. Copied in, edited by Matthew
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits

        #Handle gate sprites: kill if touching with right key.
        for wall in hits: 
            if type(wall) == Gate:
                if len(self.inventory) > 0: #Prevent NoneType error.
                    if self.getHeldItem().itemType == wall.key:
                        wall.kill()

        for wall in hits:  # if there are collisions
            #self.move_walls_x(wall)
            if self.vel.x > 0:  # moving right
                # set player position to left side of wall - player width
                self.rect.x = wall.rect.left - self.rect.width
            if self.vel.x < 0:  # moving left
                # set player position to right side of wall
                self.rect.x = wall.rect.right
            # set velocity to 0 to prevent further movement in that direction
            self.vel.x = 0
            # update rect position
            self.rect.x = self.rect.x

    def wallCollide_y(self):
        #By Ethan Ye paraphrased from cozort.
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits

        #Handle gate sprites: kill if touching with right key.
        for wall in hits: 
            if type(wall) == Gate:
                if len(self.inventory) > 0: #Prevent NoneType error.
                    if self.getHeldItem().itemType == wall.key:
                        wall.kill()

        for wall in hits:  # if there are collisions
            #self.move_walls_y(wall)
            if self.vel.y > 0:  # moving down
                # set player position to left side of wall - player width
                self.rect.y = wall.rect.top - self.rect.height
            if self.vel.y < 0:  # moving up
                # set player position to right side of wall
                self.rect.y = wall.rect.bottom
            # set velocity to 0 to prevent further movement in that direction
            self.vel.y = 0
            # update rect position
            self.rect.y = self.rect.y

    def update(self):
        #Move based on self.vel vector based on input

        #Handle movement and collision on x axis
        self.rect.x += self.vel.x
        self.wallCollide_x()

        #Handle movement and collision on y axis
        self.rect.y += self.vel.y
        self.wallCollide_y()

        #print(self.rect.x, self.rect.y)
        # print("Inventory: Length:", len(self.inventory), "Current:", self.currentItem)
        #print(self.currentItem)
        
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > settings.WINDOW_WIDTH:
            self.rect.right = settings.WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > settings.WINDOW_HEIGHT:
            self.rect.bottom = settings.WINDOW_HEIGHT
        print(self.rect.x // settings.TILESIZE, self.rect.y // settings.TILESIZE, self.game.current_map.filename)
        # print(self.inventory)

        if not (self.vel.x == 0 and self.vel.y == 0): #If the player is moving, create a fading rectangle for trail effect.
            fr = FadeRect(self.game, (255,255,255,150), settings.PLAYER_TRAIL_DECAY_RATE, self.rect.x, self.rect.y, settings.PLAYER_SIZE, settings.PLAYER_SIZE)
            self.game.all_sprites.add(fr) #Add to all_sprites group
            self.game.effect_sprites.add(fr) #Add to effect_sprites group

#Mobile entity that damages player
class Mob(pg.sprite.Sprite):
    def __init__(self, game, sizeX, sizeY, locX, locY, color, speed, health, followPlayer_bool = False):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((sizeX, sizeY))
        self.image.fill(color)  #White color for player
        self.rect = self.image.get_rect()
        self.rect.topleft = (locX, locY)

        #Set game reference
        self.game = game

        #Set mob settings
        self.speed = speed
        self.health = health

        #Boolean value that controls the behavior of the mob. False: Bounces around Map. True: Follows player.
        self.followPlayer_bool = followPlayer_bool

        self.vel = pg.Vector2() #Velocity vector

        if not self.followPlayer_bool: #Set diagonal direction
            self.angle = random.uniform(0, 2 * math.pi)
            self.vel.x = math.cos(self.angle) * self.speed #todo: Make this vector random direction
            self.vel.y = math.sin(self.angle) * self.speed

    def wallCollide_y(self):
        #By Ethan Ye paraphrased from cozort.
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            if self.vel.y > 0:  # moving down
                # set player position to left side of wall - player width
                self.rect.y = wall.rect.top - self.rect.height
            if self.vel.y < 0:  # moving up
                # set player position to right side of wall
                self.rect.y = wall.rect.bottom
            # update rect position
            self.rect.y = self.rect.y
        if len(hits) > 0: #Return true if wall was collided
            return True
        else:
            return False

    def update(self):
        print(self.rect.x, self.rect.y)
        if self.followPlayer_bool: #If mob is set to follow player
            direction = pg.Vector2(self.game.player.rect.center) - pg.Vector2(self.rect.center) #Get vector pointing from mob to player
            if direction.length() != 0:
                direction = direction.normalize() #Normalize to unit vector
                self.vel = direction * self.speed #Set velocity vector to point at player with magnitude of speed
            else:
                self.vel = pg.Vector2() #If on top of player, set velocity to 0.
        #Handle movement and collision on x axis
        self.rect.x += self.vel.x
        if self.wallCollide_x(): #If collided, bounce.
            self.vel.x *= -1

        #Handle movement and collision on y axis
        self.rect.y += self.vel.y
        if self.wallCollide_y(): #If collided, bounce.
            self.vel.y *= -1

    def wallCollide_x(self):
        #Code by Ethan Ye paraphrased from cozort. Copied in by Matthew
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            if self.vel.x > 0:  # moving right
                # set player position to left side of wall - player width
                self.rect.x = wall.rect.left - self.rect.width
            if self.vel.x < 0:  # moving left
                # set player position to right side of wall
                self.rect.x = wall.rect.right
            # update rect position
            self.rect.x = self.rect.x
        if len(hits) > 0: #Return true if wall was collided
            return True
        else:
            return False

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

        self.countdownSeconds = countdownSeconds

        self.game = game #Reference to the game to detect collidable entities

        #Divide by PLAYER_SPEED (to make all members 1), multiply by speed to get bullet velocity.
        self.velocity = pg.Vector2()
        self.velocity.x = (playerVelocity.x/settings.PLAYER_SPEED)*speed
        self.velocity.y = (playerVelocity.y/settings.PLAYER_SPEED)*speed
        self.velocity.x = (self.velocity.x/settings.PLAYER_SPEED)*speed
        self.velocity.y = (self.velocity.y/settings.PLAYER_SPEED)*speed

        #Doing it this way preserves the direction of the velocity.

    def update(self):
        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y
        
        self.countdownSeconds -= self.game.deltaTime

        if self.countdownSeconds < 0:
            self.kill() #Kill self once countdown ends
class BasicBullet(Projectile):
    def __init__(self, game, playerVelocity, x, y):
        #Construct bullet with parameters of this type of bullet:
        super().__init__(game, playerVelocity, settings.WHITE, 20, 3, x, y, 5)
    
    def update():
        pass

class Item(pg.sprite.Sprite):
    """Item class
    Author: Matthew Sheyda
    """
    def __init__(self, game, itemImage, x, y, map, itemType):
        pg.sprite.Sprite.__init__(self)
        self.itemImage = itemImage

        self.clearImage = self.image = pg.Surface((16, 16), pg.SRCALPHA) #pg.SRCALPHA allows transparancy
        self.clearImage.fill(settings.TRANSPARANT)

        self.image = itemImage #Image representing the item
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.map = map
        
        self.itemType = itemType
        self.game = game

    def update(self):
        #If in player's inventory, go to player's location.
        if self in self.game.player.inventory:
            self.rect.topleft = (self.game.player.rect.x,self.game.player.rect.y)
                
        # if item is in inventory, only show if it's held
        if self in self.game.player.inventory:
            if self.game.player.getHeldItem() == self:
                self.image = self.itemImage
            else: 
                self.image = self.clearImage
        # if item is not in inventory, only show if on current map
        else:
            if self.map == self.game.current_map:
                self.image = self.itemImage
            else:
                self.image = self.clearImage
            
#Weak sprites for easy memory management
class Wall(pg.sprite.WeakSprite):
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

class Gate(pg.sprite.WeakSprite):
    """
    Gate class
    adapted from code adapted from class code by Ethan Ye to include wall colors
    """
    def __init__(self, game, x, y, image, key):
        self.game = game
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(
            self, self.groups
        )  # initialize gate using Sprite class init function

        # gate properties (similar to wall be there's a texture)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x * settings.TILESIZE
        self.rect.y = y * settings.TILESIZE

        #The key needed to unlock this door.
        self.key = key