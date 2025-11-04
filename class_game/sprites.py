# Author: Ethan Ye

# sprites file contains classes for all sprites (mobs and players)
# separate file for modularity

# imports: pygame module, sprite module from pygame, randint from random (for mob movement) math (for mob movement) and all from settings
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from main import Game
from os import path

# from random import randint
import math
from utils import *
import random

from enum import Enum, auto

vec = pg.math.Vector2


# enum WallState class because i'm a c++ nerd
class WallState(Enum):
    STATIC = auto()
    MOVEABLE = auto()


class Bullet(Sprite):
    def __init__(self, game: Game, x: float, y: float, heading: float):
        self.game: Game = game
        self.groups = game.bullets, game.all_sprites
        Sprite.__init__(self, self.groups)
        self.speed: int = 10
        self.heading: float = heading

        self.image = pg.Surface((5, 5))
        _ = self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.vel = vec(
            math.cos(math.radians(self.heading)) * self.speed,
            math.sin(math.radians(self.heading)) * self.speed,
        )
        self.pos= vec(x, y)
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

    def update(self):
        self.pos += self.vel
        self.rect.x = int(self.pos.x)
        self.rect.y = int(self.pos.y)

        # remove bullet if collide with wall
        if pg.sprite.spritecollide(self, self.game.walls, False):
            self.kill()


# Player class
# player sprite and moves it based on wasd keystrokes


class Player(Sprite):  # player inherits from pygame Sprite class
    # initialized a Player object
    def __init__(self, game, x, y):
        self.game: Game = game
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)

        self.image = pg.Surface((32, 32))  # player is a square
        self.image.fill(RED)  # red player
        self.rect = self.image.get_rect()  # rectangle for positioning
        self.vel = vec(0, 0)  # velocity vector
        self.pos = vec(x, y) * TILESIZE[0]
        self.last_pos = self.pos.copy()  # last position vector
        self.speed = 500  # speed in pixels per second
        self.health = 10  # player health
        self.isAlive: bool = True  # whether player is alive
        # initialized a Countdown object for damage cooldown, set at 1000 ms
        self.damageCooldown = Countdown(1000)
        self.shootCountdown: Countdown = Countdown(250)
        
        self.image = SpriteSheet(path.join(self.game.img_folder, "player.png"))
        self.walking = False
        self.jumping = False
        self.last_update = 0

    def load_images (self):
        self.standing_frames = [self.spritesheet.get_image(0, 0, 32, 32),
                                self.spritesheet.get_image(32, 0, 32, 32)]

        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
    
    def animate(self):
        now = pg.time.get_ticks()
        if not self.walking and self.walking:
            if now-self.last_update > 350:
                print(now)
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        
    
    # calculate heading of player based on movement direction

    def calc_heading(self) -> float:
        dx: float = self.pos.x - self.last_pos.x
        dy: float = self.pos.y - self.last_pos.y
        heading: float = math.degrees(math.atan2(dy, dx))
        return heading

    # update Player object position based on keypresses
    def get_keys(self):
        self.vel = vec(0, 0)

        keys = pg.key.get_pressed()

        if keys[pg.K_w] and self.rect.y > 0:  # move up if not at top edge
            self.vel.y = -self.speed * self.game.dt
        if keys[pg.K_a] and self.rect.x > 0:  # move down if not at bottom edge
            self.vel.x = -self.speed * self.game.dt
        if (
            keys[pg.K_s] and self.rect.y < HEIGHT - self.rect.height
        ):  # move left if not at left edge
            self.vel.y = self.speed * self.game.dt
        if (
            keys[pg.K_d] and self.rect.x < WIDTH - self.rect.width
        ):  # move right if not at right edge
            self.vel.x = self.speed * self.game.dt

        # slow down diagonal movement
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.70710678118

        if keys[pg.K_SPACE]:
            if not self.shootCountdown.running():
                self.shootCountdown.start()
                heading: float = 0
                if self.vel.x == 0 and self.vel.y == 0:
                    heading = 0
                else:
                    heading = math.degrees(math.atan2(self.vel.y, self.vel.x))
                print("Pew Pew")
                _ = Bullet(
                    self.game,
                    self.pos.x + self.rect.width / 2,
                    self.pos.y + self.rect.height / 2,
                    heading,
                )

    # move walls if they are moveable
    def move_walls_x(self, wall):
        if wall.state == WallState.MOVEABLE:
            wall.vel.x = self.vel.x

    def move_walls_y(self, wall):
        if wall.state == WallState.MOVEABLE:
            wall.vel.y = self.vel.y

    def collide_walls_x(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            self.move_walls_x(wall)
            if self.vel.x > 0:  # moving right
                # set player position to left side of wall - player width
                self.pos.x = wall.rect.left - self.rect.width
            if self.vel.x < 0:  # moving left
                # set player position to right side of wall
                self.pos.x = wall.rect.right
            # set velocity to 0 to prevent further movement in that direction
            self.vel.x = 0
            # update rect position
            self.rect.x = self.pos.x

    def collide_walls_y(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            self.move_walls_y(wall)
            if self.vel.y > 0:  # moving down
                # set player position to top side of wall - player height
                self.pos.y = wall.rect.top - self.rect.height
            if self.vel.y < 0:  # moving up
                # set player position to bottom side of wall
                self.pos.y = wall.rect.bottom
            # set velocity to 0 to prevent further movement in that direction
            self.vel.y = 0
            # update rect position
            self.rect.y = self.pos.y

    def collide_with_walls(self, dir):
        if dir == "x":  # x direction collisions
            self.collide_walls_x()
        if dir == "y":  # y direction collisions
            self.collide_walls_y()

    def collide_with_stuff(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)  # get hits
        if hits:  # if there are collisions
            if str(hits[0].__class__.__name__) == "Mob":  # if player hit a mob
                if not self.damageCooldown.running():  # if not immune
                    self.health -= 1  # lose health
                    self.damageCooldown.start()  # start damage cooldown
                    print("Ouch")  # helpful message
            if str(hits[0].__class__.__name__) == "Coin":  # if player hit a coin
                self.game.score += 1  # increase score

    # general Player behavior
    def update(self):
        # update position based on keypress, no other behavior for now
        self.get_keys()
        # move player based on velocity vector
        self.last_pos = self.pos.copy()
        self.pos += self.vel

        # update rect x position and handle collisions with walls
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

        # update rect y position and handle collisions with walls
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        # handle collisions with mobs and coins
        self.collide_with_stuff(self.game.all_mobs, False)
        self.collide_with_stuff(self.game.coins, True)


# sprite that acts as a space invader


class Mob(Sprite):
    # initialize
    def __init__(self, game, width, length, x, y, speed, color, step):
        self.game = game  # assign game object
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(
            self, self.groups
        )  # initialize Mob using Sprite class init function

        # mob properties
        self.image = pg.Surface((width, length))  # mob is a rectangle
        self.image.fill(color)  # fill with given color
        self.rect = self.image.get_rect()  # rectangle for positioning
        self.vel = vec(
            random.choice([-1, 1]), random.choice([-1, 1])
        )  # velocity vector
        self.speed = speed  # speed
        self.pos = vec(x * 32, y * 32)  # initial position
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        self.step = step  # pixels to move down when hitting a wall

    """
    Same logic as Player collide_with_walls function, but instead of stopping movement, it bounces off walls by
    reversing (*= -1) the mob's velocity in whatever direction it hit the wall.
    """

    def collide_with_walls(self, dir):
        if dir == "x":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.rect.x = self.pos.x
                self.vel.x *= -1
        if dir == "y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.rect.y = self.pos.y
                self.vel.y *= -1

    """
    unintelligent chase logic, mob directly moves towards player at all times
    """

    def chase_player(self):
        dir = self.game.player.pos - self.pos
        dist = dir.length()

        if dist > 0:
            dir = dir.normalize()
            self.vel = dir * self.speed

        """
        previous more unintelligent chase logic, only changes direction if player is moving faster
        changes direction of y and x directly based on player's position
        """

        # if self.game.player.vel.x < self.vel.x:
        #     if self.game.player.pos.x < self.pos.x:
        #         self.vel.x = -1
        #     elif self.game.player.pos.x > self.pos.x:
        #         self.vel.x = 1

        # if self.game.player.vel.y < self.vel.y:
        #     if self.game.player.pos.y < self.pos.y:
        #         self.vel.y = -1
        #     elif self.game.player.pos.y > self.pos.y:
        #         self.vel.y = 1

    def update(self):
        # movement logic

        # update position based on velocity vector
        self.pos += self.vel * self.speed * self.game.dt

        # update rect x position and handle collisions with walls
        self.rect.x = self.pos.x
        self.collide_with_walls("x")

        # update rect y position and handle collisions with walls
        self.rect.y = self.pos.y
        self.collide_with_walls("y")

        self.chase_player()


class Coin(Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(
            self, self.groups
        )  # initialize Coin using Sprite class init function

        # coin properties
        self.image = pg.Surface((20, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]

    def update(self):
        # no movement logic for coin
        pass


class Wall(Sprite):
    def __init__(self, game, x, y, state: WallState):
        self.game = game
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(
            self, self.groups
        )  # initialize Wall using Sprite class init function

        # wall properties
        self.image = pg.Surface(TILESIZE)
        self.image.fill(GRAY)
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE[0]
        self.rect.x = x * TILESIZE[0]
        self.rect.y = y * TILESIZE[1]
        self.state = state

    """
    should only be called if wall is moveable
    similar logic to collide_with_walls function in Player and Mob classes
    moves wall in the direction of the player's movement until it hits another wall
    """

    def collide_walls_x(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            if wall == self:  # don't collide with self
                continue
            if self.vel.x > 0:  # moving right
                # set player position to left side of wall - player width
                self.pos.x = wall.rect.left - self.rect.width
            if self.vel.x < 0:  # moving left
                # set player position to right side of wall
                self.pos.x = wall.rect.right
            # set velocity to 0 to prevent further movement in that direction
            self.vel.x = 0
            # update rect position
            self.rect.x = self.pos.x

    def collide_walls_y(self):
        hits = pg.sprite.spritecollide(self, self.game.walls, False)  # get hits
        for wall in hits:  # if there are collisions
            if (
                wall == self or wall.state == WallState.MOVEABLE
            ):  # don't collide with self
                continue
            if self.vel.y > 0:  # moving down
                # set player position to top side of wall - player height
                self.pos.y = wall.rect.top - self.rect.height
            if self.vel.y < 0:  # moving up
                # set player position to bottom side of wall
                self.pos.y = wall.rect.bottom
            # set velocity to 0 to prevent further movement in that direction
            self.vel.y = 0
            # update rect position
            self.rect.y = self.pos.y

    def collide_with_other_walls(self, dir):
        if dir == "x":  # x direction collisions
            self.collide_walls_x()
        if dir == "y":  # y direction collisions
            self.collide_walls_y()

    def update(self):
        # if wall is static, do nothing
        if self.state == WallState.STATIC:
            return

        # if wall is moveable, move based on velocity vector, velocity is calculated in the player class
        self.pos += self.vel
        self.collide_with_other_walls("x")
        self.collide_with_other_walls("y")
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

        # collision logic

        self.vel = vec(0, 0)


# ScreenSaver class
# makes a sprite bounce around in an angle (similar to the old-fashioned screensaver)
class ScreenSaver(Sprite):  # inherits from pygame Sprite class
    # initialize object
    def __init__(self, game, width, length, x, y, angle, velocity, color):
        self.game = game
        self.groups = game.all_sprites, game.all_mobs
        Sprite.__init__(self, self.groups)
        self.image = pg.Surface((width, length))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = angle
        self.velocity = velocity

    # update
    # uses sine and cosine to determine the next point of the object
    def update(self):
        self.rect.x += math.cos(math.radians(self.angle)) * self.velocity
        self.rect.y += math.sin(math.radians(self.angle)) * self.velocity
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.angle = 180 - self.angle
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.angle = -self.angle
        self.angle %= 360
