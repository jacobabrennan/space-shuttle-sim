

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
from config import *


class Particle:

    def init(self, position=(0, 0, 0), radius=1):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        radius = radius

    def graphic(viewpoint):
        view_vector = vector_between(viewpoint, self.position)
        view_distance = magnitude(view_vector)
        return '@'

    def take_turn(game_time):
        pass
