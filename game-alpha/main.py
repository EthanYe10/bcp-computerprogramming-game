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
        
        #Gate images.
        self.yellowGateImage = pg.image.load(os.path.join("images", "yellowGate.png")).convert_alpha()
        self.redGateImage = pg.image.load(os.path.join("images", "redGate.png")).convert_alpha()
        self.orangeGateImage = pg.image.load(os.path.join("images", "orangeGate.png")).convert_alpha()
        self.blackGateImage =  pg.image.load(os.path.join("images", "blackGate.png")).convert_alpha()
        self.purpleGateImage =  pg.image.load(os.path.join("images", "purpleGate.png")).convert_alpha()

    def new(self): #Create a new game, sprites, and maps. 
        self.map_manager: utils.MapManager = utils.MapManager(self)

        #Area 1
        self.map1_1_1 = utils.Map(os.path.join("maps", "map1_1_1.txt"), self, fog=False)
        self.map1_2_1 = utils.Map(os.path.join("maps", "map1_2_1.txt"), self, fog=False)
        self.map1_1_2 = utils.Map(os.path.join("maps", "map1_1_2.txt"), self, fog=False)
        self.map1_1_3 = utils.Map(os.path.join("maps", "map1_1_3.txt"), self, fog=False)
        self.map1_0_4 = utils.Map(os.path.join("maps", "map1_0_4.txt"), self, fog=False)
        self.map1_1_4 = utils.Map(os.path.join("maps", "map1_1_4.txt"), self, fog=False)
        self.map1_2_4 = utils.Map(os.path.join("maps", "map1_2_4.txt"), self, fog=False)
        self.map1_2_5 = utils.Map(os.path.join("maps", "map1_2_5.txt"), self, fog=False)
        self.map1_2_6 = utils.Map(os.path.join("maps", "map1_2_6.txt"), self, fog=False)
        self.map1_3_5 = utils.Map(os.path.join("maps", "map1_3_5.txt"), self, fog=False)
        self.map1_3_2 = utils.Map(os.path.join("maps", "map1_3_2.txt"), self, fog=False)
        self.map1_0_5 = utils.Map(os.path.join("maps", "map1_0_5.txt"), self, fog=False)
        self.map1_0_2 = utils.Map(os.path.join("maps", "map1_0_2.txt"), self, fog=False)

        self.map_manager.add_map(self.map1_1_1)
        self.map_manager.add_map(self.map1_2_1)
        self.map_manager.add_map(self.map1_1_2)
        self.map_manager.add_map(self.map1_1_3)
        self.map_manager.add_map(self.map1_0_4)
        self.map_manager.add_map(self.map1_1_4)
        self.map_manager.add_map(self.map1_2_4)
        self.map_manager.add_map(self.map1_2_5)
        self.map_manager.add_map(self.map1_3_5)
        self.map_manager.add_map(self.map1_3_2)
        self.map_manager.add_map(self.map1_0_5)
        self.map_manager.add_map(self.map1_0_2)

        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1_1, self.map1_2_1, # the two maps
            24, 0,   # start of door of first map
            24, 17, # end of door of first map
            0, 0,   # start of door of second map
            0, 17, # end of door of second map
            settings.DIRECTION_RIGHT)) # the direction the player will be facing when entering the door
        
        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1_1, self.map1_1_2, # the two maps
            0, 0,   # start of door of first map
            24, 0, # end of door of first map
            0, 18,   # start of door of second map
            24, 18, # end of door of second map
            settings.DIRECTION_UP))

        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1_2, self.map1_1_3, # the two maps
            0, 0,   # start of door of first map
            24, 0, # end of door of first map
            0, 18,   # start of door of second map
            24, 18, # end of door of second map
            settings.DIRECTION_UP))

        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1_3, self.map1_0_4, # the two maps
            0, 0,   # start of door of first map
            12, 0, # end of door of first map
            0, 18,   # start of door of second map
            12, 18, # end of door of second map
            settings.DIRECTION_UP))

        self.map_manager.add_connection(utils.MapConnection(self.map1_0_4, self.map1_1_4, *settings.GENERIC_DOOR_RIGHT)) 
        self.map_manager.add_connection(utils.MapConnection(self.map1_2_4, self.map1_1_4, *settings.GENERIC_DOOR_LEFT)) 
        
        self.map_manager.add_connection(utils.MapConnection(
            self.map1_1_3, self.map1_2_4, # the two maps
            12, 0,   # start of door of first map
            24, 0, # end of door of first map
            12, 18,   # start of door of second map
            24, 18, # end of door of second map
            settings.DIRECTION_UP))

        self.map_manager.add_connection(utils.MapConnection(self.map1_2_4, self.map1_2_5, *settings.GENERIC_DOOR_UP)) 
        self.map_manager.add_connection(utils.MapConnection(self.map1_2_5, self.map1_2_6, *settings.GENERIC_DOOR_UP)) 
        self.map_manager.add_connection(utils.MapConnection(self.map1_2_5, self.map1_3_5, *settings.GENERIC_DOOR_RIGHT))
        self.map_manager.add_connection(utils.MapConnection(self.map1_3_5, self.map1_3_2, *settings.GENERIC_DOOR_DOWN))
        self.map_manager.add_connection(utils.MapConnection(self.map1_3_2, self.map1_1_2, *settings.GENERIC_DOOR_LEFT))
        self.map_manager.add_connection(utils.MapConnection(self.map1_0_4, self.map1_0_5, *settings.GENERIC_DOOR_UP))
        self.map_manager.add_connection(utils.MapConnection(self.map1_1_2, self.map1_0_2, *settings.GENERIC_DOOR_LEFT))
        
        #Using tuples that are unpacked and used as parameters for brevity.
        """
        in this example the door will be at (0,0) to (10,10) on the first map and (0,0) to (10,10) on the second map
        thus if the player is in the first map and their position is anywhere from (0,0) to (10,10) the player will be teleported to the second map at (0,0)
        """
        self.current_map = self.map1_1_1
        
        #Create sprite groups
        self.all_sprites = pg.sprite.Group() #Sprite group which contains all sprites

        self.input_sprites = pg.sprite.Group() #Sprite group which contains all sprites with input() from the user
        
        self.visible_sprites = pg.sprite.Group() #Sprite group for all visible sprites (if there is fog of war)

        self.item_sprites = pg.sprite.Group() #Sprite group for items 

        self.effect_sprites = pg.sprite.Group() #Sprite group for visual effects related sprites

        self.projectile_sprites = pg.sprite.Group() #Sprite group for projectile sprites
        
        self.walls = pg.sprite.Group() #Sprite group for walls

        self.mob_sprites = pg.sprite.Group() #Sprite group for mobs

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
        img = pg.image.load(os.path.join("images", "redKey.png")).convert_alpha()
        itm = Item(self, img, 350, 350, self.map1_2_1, settings.ITEM_TYPE_KEY_RED)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)
        self.load_map(self.current_map)

        #Black key
        img = pg.image.load(os.path.join("images", "blackKey.png")).convert_alpha()
        itm = Item(self, img, 50, 350, self.map1_3_2, settings.ITEM_TYPE_KEY_BLACK)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Yellow Key
        img = pg.image.load(os.path.join("images", "yellowKey.png")).convert_alpha()
        itm = Item(self, img, 400, 64, self.map1_2_6, settings.ITEM_TYPE_KEY_YELLOW)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Orange Key
        img = pg.image.load(os.path.join("images", "orangeKey.png")).convert_alpha()
        itm = Item(self, img, 400, 300, self.map1_3_2, settings.ITEM_TYPE_KEY_ORANGE)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Weapon Tesla
        img = pg.image.load(os.path.join("images", "weapon_tesla.png")).convert_alpha()
        itm = Item(self, img, 64, 300, self.map1_0_2, settings.ITEM_TYPE_WEAPON_TESLA)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

        #Purple Key
        img = pg.image.load(os.path.join("images", "purpleKey.png")).convert_alpha()
        itm = Item(self, img, 200, 64, self.map1_0_5, settings.ITEM_TYPE_KEY_PURPLE)
        self.all_sprites.add(itm)
        self.item_sprites.add(itm)

    def input(self):
        #Loop through all sprites that take input and scan for input.
        for sprite in self.input_sprites:
            sprite.input()
        pass
    def update(self):
        #run update function of all sprites
        
        if self.current_map.fog:
            self.visible_sprites.empty()
            for sprite in self.all_sprites:
                x_diff = self.player.rect.x - sprite.rect.x 
                y_diff = self.player.rect.y - sprite.rect.y 
                dist = ((x_diff)**2 + (y_diff)**2)**0.5
                if dist <= settings.FOG_RADIUS_TILES * settings.TILESIZE:
                    self.visible_sprites.add(sprite)
            self.visible_sprites.update()
        else:
            self.all_sprites.update()
                
        self.check_map_transitions()


    def draw(self):
        if self.current_map.fog:
            # fill screen with blue underlay
            self.screen.fill(settings.BLUE)
            # draw visible sprites
            self.visible_sprites.draw(self.screen)
            
            # new surface for fog (layer above blue underlay)
            fog_surface = pg.Surface((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT), pg.SRCALPHA)
            fog_surface.fill(settings.DARK_GRAY)
            
            # circle around player to clear fog
            player_center_x = self.player.rect.centerx
            player_center_y = self.player.rect.centery
            clear_radius = settings.FOG_RADIUS_TILES * settings.TILESIZE
            
            # transparent circle 
            pg.draw.circle(fog_surface, settings.TRANSPARANT, (player_center_x, player_center_y), clear_radius)
            
            # TODO: implement gradient effect
            gradient_steps = 15
            
            self.screen.blit(fog_surface, (0, 0))
            
        else:
            self.screen.fill(settings.BLUE)
            #Draw sprites in specific order to prevent layering issues.
            self.effect_sprites.draw(self.screen)
            self.input_sprites.draw(self.screen)
            self.item_sprites.draw(self.screen)
            self.projectile_sprites.draw(self.screen)
            self.walls.draw(self.screen)
            self.mob_sprites.draw(self.screen)
        pg.display.flip()

    def clear_map(self):
        """
        Clears all sprite groups not common to all maps and walls while loading the next map in a map transition
        specifically, it clears walls, effects, TODO: other items to be cleared
        Author: Ethan Ye, Matthew Sheyda"""
        self.effect_sprites.empty()
        self.walls.empty()
        self.mob_sprites.empty()

        #Kill all of those sprites, now.
        for sprite in self.all_sprites:
            if type(sprite) == Wall or type(sprite) == Gate or type(sprite) == Mob or type(sprite) == FadeRect: 
                sprite.kill()

    def check_map_transitions(self):
        """
        Checks if player is within the "door zone" of the current map and assign next_map to the next map if applicable, None if not. 
        Teleports player to the other map and updates and loads the next map
        Author: Ethan Ye
        
        Edited for seemless transitions by Matthew Sheyda:
        get_connected_map() now returns direction also. Direction is checked to apply door boost and 
        interpolate along the axis that runs parrelel to the doors' directions.
        """
        
        next_map, spawnX, spawnY = self.map_manager.get_connected_map(self.current_map, self.player.rect.x//settings.TILESIZE, self.player.rect.y//settings.TILESIZE)
        if next_map and next_map != self.current_map:
            print("Transitioning to map:", next_map.filename)
            print('Player', self.player.rect.x // settings.TILESIZE, self.player.rect.y // settings.TILESIZE)
            self.clear_map()
            self.load_map(next_map)
            self.current_map = next_map
            
            self.player.rect.x = spawnX
            self.player.rect.y = spawnY

    def load_map(self, map : utils.Map):
        """
        Loads the sprites and data from a Map object's data attribute
        Adapted from class Game
        Author: Ethan Ye"""

        #Iterate through the map file. Spawn the corresponding wall/gray/enemy.
        for row, tiles in enumerate(map.data):
            for col, tile in enumerate(tiles):
                if tile == "1": #Wall (Light Gray)
                    _ = Wall(self, col, row, settings.LIGHT_GRAY)
                if tile == "2": #Wall (Dark Gray)
                    _ = Wall(self, col, row, settings.DARK_GRAY)
                if tile == "3": #Wall (Dark Purple)
                    _ = Wall(self, col, row, settings.DEEP_PURPLE)
                if tile == "r": #Gate (Red)
                    _ = Gate(self, col, row, self.redGateImage, settings.ITEM_TYPE_KEY_RED)
                if tile == "y": #Gate (Yellow)
                    _ = Gate(self, col, row, self.yellowGateImage, settings.ITEM_TYPE_KEY_YELLOW)
                if tile == "o": #Gate (Orange)
                    _ = Gate(self, col, row, self.orangeGateImage, settings.ITEM_TYPE_KEY_ORANGE)
                if tile == "b": #Gate (Blue)
                    _ = Gate(self, col, row, self.blackGateImage, settings.ITEM_TYPE_KEY_BLACK)
                if tile == "p": #Gate (Purple)
                    _ = Gate(self, col, row, self.purpleGateImage, settings.ITEM_TYPE_KEY_PURPLE)
                if tile == "e": #Enemy (Standard)
                    pass #_ = Gate(self, col, row, self.purpleGateImage, settings.ITEM_TYPE_KEY_PURPLE)
                    
g = Game()
g.new()

while not pg.event.peek(pg.QUIT): #Checks if there is a quit event in events (User wants to exit).
    g.deltaTime = g.clock.tick(settings.FPS) / 1000

    g.input()
    g.update()
    g.draw()