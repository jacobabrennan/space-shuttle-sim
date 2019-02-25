

# = Particle ==================================================================
"""
Particles are the base class for game objects. They function perfectly as stars
and planets without any sub-classing. Mass must be specified in order to exert
a gravitational force. Distant stars should not have mass, so as to increase
performance.
"""


# - Dependencies ---------------------------------
# Python Modules
import math
import random
# Local Modules
from config import *
from vector3d import *


class Particle:
    """
    The parent type of most game objects. A sphere with position in space.
    Particles will display at a location in space, with a given radius. If a
    mass is specified, the particle will exert an attractive force on all
    vehicles.

    Currently, the label property can be set to display a string near the
    particle. This is useful for showing the player the position of particles
    against the backdrop of stars. This behavior may soon change.
    """

    def __init__(self, position=(0, 0, 0), radius=1, mass=0):
        if(position):
            self.position = tuple(position)
        else:
            self.position = (0, 0, 0)
        self.radius = radius
        self.mass = mass
        self.label = None

    def take_turn(self, game_time):
        """Provides a hook for code to execute every game loop iteration."""
        pass
