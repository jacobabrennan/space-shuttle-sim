

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
# from config import *
from vector3d import *


class Particle:

    def __init__(self, position=(0, 0, 0), radius=1):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        radius = radius

    def graphic(self, viewpoint, bearing, attitude, starboard):
        # Translate position into terms of viewpoint coordinates
        delta_position = vector_between(viewpoint, self.position)
        relative_position = (
            scalar_product(delta_position, starboard),
            scalar_product(delta_position, attitude),
            scalar_product(delta_position, bearing),
        )

        #
        if(relative_position[2] <= 0):
            return None
        #
        scale = 1 / relative_position[2]
        display_position = (
            relative_position[0]*scale,
            relative_position[1]*scale,
        )
        #
        return ('@', display_position)

    def take_turn(self, game_time):
        pass
