# Created by Ethan Ye with the help of Claude and Gemini specifically
# I swear I didn't use ChatGPT for this...

import math
import random
from os import path
import string
import pygame as pg

from settings import *
from sprites import *
from utils import Map, Countdown


class Game:
    def __init__(self):
        _ = pg.init()  # init pygame
        self.time: int = 0

        # initialize stuff to keep linting happy

        self.game_folder: str = ""
        self.map: Map | None = None
        self.all_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.player = None
        self.dt = 0

        self.clock = pg.time.Clock()  # clock to control frame rate
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))  # set screen dimensions
        self.score = 0  # initialize score
        
        # this caption made using ChatGPT
        pg.display.set_caption(
            "Ethan Ye's amazing breathtaking captivating dazzling exceptional fantastic glorious heroic incredible jaw-dropping knockout legendary marvelous noteworthy outstanding phenomenal quality remarkable stunning tremendous unbelievable visionary wonderful exceptional youthful zestful game"
        )
        self.playing = True  # game loop boolean
        

    # sets up game folder dir using current folder containing THIS file
    # gives the game class a map property that uses Map class to parse level1.txt file
    def load_data(self):
        self.game_folder = path.dirname(__file__)
        self.map = Map(path.join(self.game_folder, "levels/level1.txt"))
        self.img_folder = path.join(self.game_folder, "images")
        self.player_image = path.join(self.img_folder, "player.png")
        
        

    def new(self):
        self.load_data()

        # create all sprite groups
        self.all_sprites = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.all_mobs = pg.sprite.Group()

        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                # create sprites based on data in the file
                if tile == "1":
                    _ = Wall(self, col, row, WallState.STATIC)

                if tile == "2":
                    _ = Wall(self, col, row, WallState.MOVEABLE)
                if tile == "C":  # coin
                    _ = Coin(self, col, row)
                if tile == "M":  # mob
                    color = (
                        random.randint(0, 255),
                        random.randint(0, 255),
                        random.randint(0, 255),
                    )
                    # _ = Mob(self, 32, 32, col, row, 10, color, 10)
                if tile == "P":  # player
                    self.player = Player(self, col, row)

    def run(self):
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            self.events()  # check for events
            self.update()  # update game state
            self.draw()  # draw updates to the screen
        pg.quit()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:  # if the window is closed
                self.playing = False

    def update(self):
        self.all_sprites.update()  # update all sprites
        self.all_mobs.update()  # update all mobs
        self.coins.update()  # update all coins
        self.bullets.update()  # update all bullets

        self.time = pg.time.get_ticks()

        if self.player.health <= 0:  # death and game over if health is 0
            self.draw_text(self.screen, "Game Over", 100, RED, WIDTH / 2, HEIGHT / 2)
            pg.display.flip()
            pg.time.delay(2000)
            self.playing = False

    def draw(self):
        self.screen.fill(LIGHT_GRAY)  # light gray screen
        self.all_sprites.draw(self.screen)  # draw all sprites
        self.all_mobs.draw(self.screen)  # draw all mobs
        self.coins.draw(self.screen)  # draw all coins
        self.bullets.draw(self.screen)
        self.draw_text(
            self.screen, "Score: " + str(self.score), 22, BLACK, WIDTH / 2, 10
        )  # draw score
        self.draw_text(
            self.screen,
            "Health: " + str(self.player.health),
            22,
            BLACK,
            WIDTH - 100,
            10,
        )  # draw health
        self.draw_text(
            self.screen, "Time: " + str(self.time), 22, BLACK, 100, 100
        )  # draw in-game time

        pg.display.flip()  # update the full display to the screen

    # teacher written function
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font("arial")
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)


if __name__ == "__main__":
    # create instance of game class/instantiating game class
    g = Game()
    g.new()
    # loop runs while playing is true
    g.run()
