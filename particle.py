

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

    def graphic(self, viewpoint, orientation):
        # view_vector = vector_between(viewpoint, self.position)
        # view_distance = magnitude(view_vector)
        orientation_distance = scalar_projection_3d(
            vector_between_3d(viewpoint, self.position),
            orientation,
        )
        reference_point = scale_vector_3d(orientation, orientation_distance)
        orthogonal_distance = distance_3d(self.position, reference_point)
        return '@'

    def take_turn(self, game_time):
        pass
