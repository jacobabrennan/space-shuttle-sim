

# = Vehicle ===================================================================

# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
from config import *
from vector3d import *
from particle import Particle
import game


class Vehicle(Particle):

    def __init__(self, position=(0, 0, 0)):
        super().__init__(position)
        # By default, the vehicle is stationary, facing forward, and upright.
        self.velocity = (0, 0, 0)
        self.angular_velocity = (0, 0, 0)  # Radians per tick
        self.bearing = (0, 0, 1)
        self.attitude = (0, 1, 0)
        self.radius = -1  # Quirk so ship is "behind" viewpoint.
        the_game = game.get_game()
        the_game.vehicles.append(self)

    def pitch(self, radians):
        """Adjusts bearing & attitude by rotating about the X/lateral axis."""
        new_bearing = vector_addition(
            scale_vector(self.bearing, math.cos(radians)),
            scale_vector(self.attitude, math.sin(radians)),
        )
        self.attitude = vector_addition(
            scale_vector(self.bearing, math.cos(radians+math.pi/2)),
            scale_vector(self.attitude, math.sin(radians+math.pi/2)),
        )
        self.bearing = new_bearing

    def yaw(self, radians):
        """Adjusts bearing & attitude by rotating about the Y/vertical axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.bearing = vector_addition(
            scale_vector(starboard, math.cos(radians+math.pi/2)),
            scale_vector(self.bearing, math.sin(radians+math.pi/2)),
        )

    def roll(self, radians):
        """Adjusts bearing & attitude by rotating about the Z/forward axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.attitude = vector_addition(
            scale_vector(starboard, math.cos(radians+math.pi/2)),
            scale_vector(self.attitude, math.sin(radians+math.pi/2)),
        )

    # def graphic(viewpoint, ):
    #     distance = math.sqrt(x**2 + y**2 + z**2)
    #     return '#'

    def take_turn(self, game_time):
        # Apply rotations
        if(self.angular_velocity[0]):
            self.pitch(self.angular_velocity[0])
        if(self.angular_velocity[1]):
            self.yaw(self.angular_velocity[1])
        if(self.angular_velocity[2]):
            self.roll(self.angular_velocity[2])
        # Apply translations
        self.position = vector_addition(self.position, self.velocity)
    
    def exert_gravity(self, vehicles, time_interval):
        pass
