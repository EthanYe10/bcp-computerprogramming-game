# resolution of each tile
TILESIZE = 32

PLAYER_SPEED = 10

PLAYER_SIZE = 32
PLAYER_TRAIL_DECAY_RATE = 2

MAX_INVENTORY_ITEMS = 2

# default colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
WHITE_OPAQUE = (255, 255, 255, 255)
TRANSPARANT = (0, 0, 0, 0)
TILE_SIZE = 32

# game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

DIRECTION_UP = 1
DIRECTION_DOWN = 2
DIRECTION_LEFT = 3
DIRECTION_RIGHT = 4
DIRECTION_TOPLEFT = 5
DIRECTION_DOWNLEFT = 6
DIRECTION_TOPRIGHT = 7
DIRECTION_DOWNRIGHT = 8

DOOR_BOOST = 50
"""Small boost for when the player transitions maps 
through a connection to prevent being placed in the 
zone of the opposite door, thereby getting stuck loop of
transitioning between the two doors."""

ITEM_TYPE_KEY_BLACK = 1
ITEM_TYPE_KEY_RED = 2
ITEM_TYPE_KEY_YELLOW = 3
ITEM_TYPE_WEAPON_TESLA = 4

FOG_RADIUS_TILES = 2