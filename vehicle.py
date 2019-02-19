

# = Vehicle ===================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
from config import *
from particle import Particle


class Vehicle(Particle):

    def init(self, position):
        super().__init__(position)
        self.velocity = (0, 0, 0)
        self.orientation = (0, 0, 1)

    # def graphic(viewpoint, ):
    #     distance = math.sqrt(x**2 + y**2 + z**2)
    #     return '#'
