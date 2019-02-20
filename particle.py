

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
import random
# Local Modules
from config import *
from vector3d import *


class Particle:

    def __init__(self, position=(0, 0, 0), radius=1):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        self.radius = radius

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
        apparent_size = scale * self.radius * 2
        pixel_size = apparent_size * SCREEN_PIXEL_WIDTH/SCREEN_PHYSICAL_WIDTH
        # ^ Only width is needed as all particles are spheres
        graphic = None
        if(pixel_size >= 6):
            graphic = '@'
        elif(pixel_size >= 5):
            graphic = 'o'
        elif(pixel_size >= 4):
            graphic = '•'
            # °*+@Oo©®
        elif(pixel_size >= 3 and random.random() < 1/8):
            graphic = random.choice(('+', '×'))
        else:
            graphic = '·'
        #
        return (graphic, display_position)

    def take_turn(self, game_time):
        pass
