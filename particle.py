

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
import random
# Local Modules
from config import *
from vector3d import *


class Particle:

    def __init__(self, position=(0, 0, 0), radius=1, mass=0):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        self.radius = radius
        self.mass = mass
        self.label = None

    def take_turn(self, game_time):
        pass

    def sprite(self, radius, position):
        pass
