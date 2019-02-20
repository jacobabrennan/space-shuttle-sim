

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

    def graphic(self, relative_position):
        if(pixel_radius < CHARACTER_WIDTH*2):
            return self.graphic_simple(pixel_radius, pixel_position)
        else:
            return self.graphic_large(pixel_radius, pixel_position)

    def graphic_simple(self, pixel_radius, pixel_position):
        character_position = (
            pixel_position[0] / CHARACTER_WIDTH,
            pixel_position[1] / CHARACTER_HEIGHT,
            pixel_position[2],
        )  # Offset from origin, in terms of characters (Y axis points up)
        sprite = None
        if(pixel_radius >= 6):
            sprite = '@'
        elif(pixel_radius >= 5):
            sprite = 'o'
        elif(pixel_radius >= 4):
            sprite = '•'
            # °*+@Oo©®
        elif(pixel_radius >= 3/4 and random.random() < 1/8):
            sprite = random.choice(('+', '×'))
        # elif(pixel_radius >= 1/50):
        #     sprite = '·'
        else:
            sprite = '·'
        #
        return (sprite, character_position)

    def graphic_large(self, pixel_radius, pixel_position):
        character_position = (
            pixel_position[0] / CHARACTER_WIDTH,
            pixel_position[1] / CHARACTER_HEIGHT,
            pixel_position[2],
        )  # Offset from origin, in terms of characters (Y axis points up)
        left_edge = (pixel_position[0] - pixel_radius) / CHARACTER_WIDTH
        right_edge = (pixel_position[0] + pixel_radius) / CHARACTER_WIDTH
        top_edge = (pixel_position[1] - pixel_radius) / CHARACTER_HEIGHT
        bottom_edge = (pixel_position[1] + pixel_radius) / CHARACTER_HEIGHT
        chars_height = (right_edge - left_edge) + 1
        chars_width = (top_edge - bottom_edge) + 1
        graphic = [None] * int(chars_width*chars_height)
        for compound_index in range(len(graphic)):
            posX = compound_index % chars_width  # Left to right
            posY = math.floor(compound_index / chars_width)  # Bottom up
            graphic[compound_index] = '#'
        return (None, character_position, (graphic, chars_width, chars_height))

    def take_turn(self, game_time):
        pass
