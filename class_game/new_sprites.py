import pygame as pg
from pygame.sprite import Sprite

import math
import random

from main import Game
from utils import Countdown
import settings as S

from enum import Enum, auto

# pygame vector for speed and position
vector = pg.math.Vector2


# wall states for different wall types
# enum because i'm a c++ nerd
class WallState(Enum):
    STATIC = auto()
    MOVEABLE = auto()


class Bullet(Sprite):
    def __init__(self, game: Game, pos: vector, velocity: vector):
        self.groups = game.bullets
