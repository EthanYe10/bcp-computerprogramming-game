import pygame as pg
from os import path
from settings import *

class Map:
    """class Map
    partially written in class by Mr. Cozort
    other portions paraphrased by various sources by Ethan Ye"""
    
    # initialize map object from text file
    def __init__(self, filename):
        self.filename = filename
        # data is list of strings
        self.data = []

        # load map from file, using 'with' to ensure file is closed after reading
        with open(filename, "rt") as f1:

            # read each line from the file, strip whitespace, and append to data list
            for line in f1:
                self.data.append(line.strip())

            # set map dimensions based on data
            # dimensions are 32 pixels per tile
            self.tilewidth = len(self.data[0])
            self.tileheight = len(self.data)
            self.width = self.tilewidth * 32
            self.height = self.tileheight * 32
    
    def find_tile(self, tile_char):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == tile_char:
                    return (i, j)
        return None

    
                

class MapConnection:
    """class MapConnection
    author: Ethan Ye
    this class declares a connection between two maps
    more of a struct than a class, declare multiple if you value your sanity
    """
    def __init__(self, map1: Map, map2: Map, 
                 map1x1, map1y1, map1x2, map1y2, 
                 map2x1, map2y1, map2x2, map2y2, 
                 direction): 
        """initializes map connection
        map1 and map2 are the maps connected
        map1x1, map1y1, map1x2, map1y2 are coordinates in the map valid for the door on map1
        map2x1, map2y1, map2x2, map2y2 are coordinates in the map valid for the door on map2

        when a player enters a door they always exit at the other maps x1, y1

        direction is the direction the player will be facing when entering the door
        """
        self.map1 = map1
        self.map2 = map2
        self.map1x1 = map1x1
        self.map1y1 = map1y1
        self.map1x2 = map1x2
        self.map1y2 = map1y2
        self.map2x1 = map2x1
        self.map2y1 = map2y1
        self.map2x2 = map2x2
        self.map2y2 = map2y2
        self.direction = direction


class MapManager:
    """class MapManager
    author: Ethan Ye
    this class handles map connections and declares player movement between maps
    singleton instance, do not create multiple if you values your sanity
    contains functions to add maps and connections, and get the next map if player is in a door
    """
    def __init__(self):
        self.maps = {}
        self.connections = []
    
    def add_map(self, map: Map):
        """add a map to the map manager"""
        self.maps[map.filename] = map
    
    def add_connection(self, connection: MapConnection):
        """add a connection between two maps"""
        self.connections.append(connection)
    
    def get_connected_map(self, map: Map, player_x, player_y):
        """returns connected map if player is in the door
        should be called every game loop to check if player is in a door
        if player is in a door return the next map, else return None

        set up like this: 
        map_graph = MapManager() # SINGLETON
        map1 = Map("map1.txt")
        map2 = Map("map2.txt")
        map_graph.add_map(map1)
        map_graph.add_map(map2)
        map_graph.add_connection(MapConnection(map1, map2, 0, 0, 10, 10, 0, 0, 10, 10, "right"))

        then in the main loop run 
        next_map = map_graph.get_connected_map(player.current_map, player.rect.x, player.rect.y)

        if next_map is not None:
            player.current_map = next_map
            player.rect.x = next_map.map2x1
            player.rect.y = next_map.map2y1
            # load next map
        """
        for connection in self.connections:
            if (connection.map1 == map and
                connection.map1x1 <= player_x <= connection.map1x2 and
                connection.map1y1 <= player_y <= connection.map1y2):
                return connection.map2
            if (connection.map2 == map and
                connection.map2x1 <= player_x <= connection.map2x2 and
                connection.map2y1 <= player_y <= connection.map2y2):
                return connection.map1
        return None
    

class Countdown:
    """class Countdown
    author: Mr. Cozort
    countdown timer class 
    example usage:
    countdown = Countdown(5000)  # 5 seconds
    if damaged:
        countdown.start()
        invincible = true
    if countdown.running():
        # player is invincible
    """
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
    """class SpriteSheet
    author: Mr. Cozort
    """
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0,0), (x,y, width, height))
        image = pg.transform.scale(image, (width // 2, height // 2))
        return image

def read_data(filename):
    """read data from a file and returns it as an array of strings
    author: Ethan Ye
    """
    data = []
    with open(filename, "r") as f:
        for line in f:
            data.append(line.strip())
    return data

def write_data(filename, data):
    """write data to a file and also truncates the file
    author: Ethan Ye
    """
    with open(filename, "w") as f:
        for line in data:
            f.write(line + "\n")

def append_data(filename, data):
    """append data to a file
    author: Ethan Ye
    """
    with open(filename, "a") as f:
        for line in data:
            f.write(line + "\n")

def write_data_at_position(filename, data, x, y):
    """writes data to a specific positiom
    first deletes data at that position as well as the following data on that line 
    does this in order to replace data at the position
    author: Ethan Ye"""
    pass