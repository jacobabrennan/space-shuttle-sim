

# = Particle ==================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
# from config import *
from vector3d import *


class Particle:

    def init(self, position=(0, 0, 0), radius=1):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        radius = radius

    def graphic(self, viewpoint, bearing):
        # view_vector = vector_between(viewpoint, self.position)
        # view_distance = magnitude(view_vector)
        bearing_distance = scalar_projection(
            vector_between(viewpoint, self.position),
            bearing,
        )
        reference_point = scale_vector(bearing, bearing_distance)
        orthogonal_distance = distance(self.position, reference_point)
        return '@'

    def take_turn(self, game_time):
        pass
