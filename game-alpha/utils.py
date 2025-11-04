import pygame as pg
from os import path
from settings import *

# map class loads map from text file and sets dimensions
class Map:
    # initialize map object from text file
    def __init__(self, filename):
        # data is list of strings
        self.data = []

        # load map from file, using 'with' to ensure file is closed after reading
        with open(filename, "rt") as f:

            # read each line from the file, strip whitespace, and append to data list
            for line in f:
                self.data.append(line.strip())

            # set map dimensions based on data
            # dimensions are 32 pixels per tile
            self.tilewidth = len(self.data[0])
            self.tileheight = len(self.data)
            self.width = self.tilewidth * 32
            self.height = self.tileheight * 32
        
        self.discovered = [[False for _ in range(self.tilewidth)] for _ in range(self.tileheight)]
    
    def load_map(self, filename):
        # for line in self.data:
        #     for tile in line:
                
        #         if tile == 'P':
        #             print("Player found")
        #             # init player
        #         if tile == '1':
        #             print("Wall found")
        #             # init wall
        #         if tile == '.':
        #             print("Empty space found")
        #             # do nothing
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if not self.discovered[i][j]:
                    print("not discovered", i, j)
                    continue
                tile = self.data[i][j]
                if tile == 'P':
                    print("Player found at", i, j)
                if tile == '1':
                    print("Wall found at", i, j)
                if tile == '.':
                    print("Empty space found at", i, j)
                
        
# countdown timer class 
# example usage:
# countdown = Countdown(5000)  # 5 seconds
# if damaged:
#     countdown.start()
#     invincible = true
# if countdown.running():
#     # player is invincible
class Countdown:
    def __init__(self, time):
        self.time = time
        self.start_time = 0
        self.isRunning = False
        
    def start(self):
        self.start_time = pg.time.get_ticks()
        self.isRunning = True
    
    def running(self):
        now = pg.time.get_ticks()
        if now - self.start_time >= self.time:
            self.isRunning = False
        return self.isRunning
            
        
class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image
    
