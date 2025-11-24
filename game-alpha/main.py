import pygame as pg
import settings
import utils
from sprites import *
import os

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        # initialize map manager

    def new(self): #Create a new game, sprites, and maps. 
        self.map_manager: utils.MapManager = utils.MapManager()

        self.map1_1 = utils.Map(os.path.join("maps", "map1_1.txt"))
        self.map1_2 = utils.Map(os.path.join("maps", "map1_2.txt"))

        self.map_manager.add_map(self.map1_1)
        self.map_manager.add_map(self.map1_2)

        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1, self.map1_2, # the two maps
            24, 0,   # start of door of first map
            24, 17, # end of door of first map
            0, 0,   # start of door of second map
            0, 17, # end of door of second map
            "right")) # the direction the player will be facing when entering the door
        """
        in this example the door will be at (0,0) to (10,10) on the first map and (0,0) to (10,10) on the second map
        thus if the player is in the first map and their position is anywhere from (0,0) to (10,10) the player will be teleported to the second map at (0,0)
        """
        self.current_map = self.map1_1
        
        #Create sprite groups
        self.all_sprites = pg.sprite.Group() #Sprite group which contains all sprites

        self.input_sprites = pg.sprite.Group() #Sprite group which contains all sprites with input() from the user

        self.item_sprites = pg.sprite.Group() #Sprite group for items 

        self.effect_sprites = pg.sprite.Group() #Sprite group for visual effects related sprites

        self.projectile_sprites = pg.sprite.Group() #Sprite group for projectile sprites
        self.walls = pg.sprite.Group() #Sprite group for walls

        #Instantiate Player, add to sprite groups.
        self.player = Player(self, 200, 200) #Store player reference for later access
        self.input_sprites.add(self.player)
        self.all_sprites.add(self.player)

        #Create delta time and pg.Clock attributes.
        self.deltaTime = 0
        g.clock = pg.time.Clock()
        
        self.map_transition_countdown = utils.Countdown(500) # 500 ms countdown for map transitions

        #Create items:

        #Red key
        img = pg.image.load("images\\blackKey.png").convert_alpha()
        itm = Item(self, img, 200, 200, 0, 0, settings.ITEM_TYPE_KEY_BLACK)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)
        self.load_map(self.current_map)

        #Black key
        img = pg.image.load("images\\redKey.png").convert_alpha()
        itm = Item(self, img, 300, 300, 0, 0, settings.ITEM_TYPE_KEY_BLACK)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Yellow Key
        img = pg.image.load("images\\yellowKey.png").convert_alpha()
        itm = Item(self, img, 400, 400, 0, 0, settings.ITEM_TYPE_KEY_BLACK)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Weapon Tesla
        img = pg.image.load("images\\weapon_tesla.png").convert_alpha()
        itm = Item(self, img, 500, 500, 0, 0, settings.ITEM_TYPE_WEAPON_TESLA)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

    def input(self):
        #Loop through all sprites that take input and scan for input.
        for sprite in self.input_sprites:
            sprite.input()
        pass
    def update(self):
        #run update function of all sprites
        print(self.player.rect.x // settings.TILESIZE, self.player.rect.y // settings.TILESIZE)
        for sprite in self.all_sprites:
            sprite.update()
        self.check_map_transitions()
    def draw(self):
        self.screen.fill(settings.BLUE)
        #Draw sprites in specific order to prevent layering issues.
        self.effect_sprites.draw(self.screen)
        self.input_sprites.draw(self.screen)
        self.item_sprites.draw(self.screen)
        self.projectile_sprites.draw(self.screen)
        self.walls.draw(self.screen)
        pg.display.flip()

    def clear_map(self):
        """
        Clears all sprite groups not common to all maps and walls while loading the next map in a map transition
        specifically, it clears walls, effects, TODO: other items to be cleared
        Author: Ethan Ye"""
        self.effect_sprites.empty()
        self.walls.empty()

    def check_map_transitions(self):
        """
        Checks if player is within the "door zone" of the current map and assign next_map to the next map if applicable, None if not. 
        Teleports player to the other map and updates and loads the next map
        Author: Ethan Ye"""
        
        if self.map_transition_countdown.running():
            return
        self.map_transition_countdown.start()
        next_map, spawnX, spawnY = self.map_manager.get_connected_map(self.current_map, self.player.rect.x//settings.TILESIZE, self.player.rect.y//settings.TILESIZE)
        if next_map and next_map != self.current_map:
            print("Transitioning to map:", next_map.filename)
            print('Player', self.player.rect.x // settings.TILESIZE, self.player.rect.y // settings.TILESIZE)
            self.clear_map()
            self.load_map(next_map)
            self.current_map = next_map
            self.player.rect.x = spawnX * settings.TILESIZE
            self.player.rect.y = spawnY * settings.TILESIZE

    def load_map(self, map : utils.Map):
        """
        Loads the sprites and data from a Map object's data attribute
        Adapted from class Game
        Author: Ethan Ye"""
        for row, tiles in enumerate(map.data):
            for col, tile in enumerate(tiles):
                if tile == "1":
                    _ = Wall(self, col, row, settings.LIGHT_GRAY)
                if tile == "2":
                    _ = Wall(self, col, row, settings.DARK_GRAY)

            

g = Game()
g.new()

while not pg.event.peek(pg.QUIT): #Checks if there is a quit event in events (User wants to exit).
    g.deltaTime = g.clock.tick(settings.FPS) / 1000

    g.input()
    g.update()
    g.draw()