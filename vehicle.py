

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
        self.gravitational_reference = None
        self.fine_control_display = [0, 0, 0]
        self.main_thruster_output = 0
        the_game = game.get_game()
        the_game.vehicles.append(self)

    def increase_thrust(self, force):
        """Adjusts the current (ongoing) output of the main thrusters."""
        self.main_thruster_output += force

    def pitch(self, radians):
        """Adjusts angular velocity about the X/lateral axis."""
        self.angular_velocity = (
            self.angular_velocity[0]+radians,
            self.angular_velocity[1],
            self.angular_velocity[2],
        )
        self.fine_control_display[0] += radians/SHIP_TURNING_ANGLE

    def yaw(self, radians):
        """Adjusts angular velocity about the Y/vertical axis."""
        self.angular_velocity = (
            self.angular_velocity[0],
            self.angular_velocity[1]+radians,
            self.angular_velocity[2],
        )
        self.fine_control_display[1] += radians/SHIP_TURNING_ANGLE

    def roll(self, radians):
        """Adjusts angular velocity about the Z/forward axis."""
        self.angular_velocity = (
            self.angular_velocity[0],
            self.angular_velocity[1],
            self.angular_velocity[2]+radians,
        )
        self.fine_control_display[2] += radians/SHIP_TURNING_ANGLE

    def thrust(self, force, time_interval):
        """
        Changes instantaneous velocity by Accelerating the vehicle along its
        bearing vector. Use negative force for slowing down and reverse.
        """
        # F = ma
        # a = v/t
        A = force/self.mass
        V = A * time_interval
        V = scale_vector(self.bearing, V)
        self.velocity = vector_addition(self.velocity, V)

    def adjust_pitch(self, radians):
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

    def adjust_yaw(self, radians):
        """Adjusts bearing & attitude by rotating about the Y/vertical axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.bearing = vector_addition(
            scale_vector(starboard, math.cos(radians+math.pi/2)),
            scale_vector(self.bearing, math.sin(radians+math.pi/2)),
        )

    def adjust_roll(self, radians):
        """Adjusts bearing & attitude by rotating about the Z/forward axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.attitude = vector_addition(
            scale_vector(starboard, math.cos(radians+math.pi/2)),
            scale_vector(self.attitude, math.sin(radians+math.pi/2)),
        )

    def take_turn(self, game_time):
        # Apply Thrust
        if(self.main_thruster_output):
            self.thrust(self.main_thruster_output, game_time)
        # Apply rotations
        if(self.angular_velocity[0]):
            self.adjust_pitch(self.angular_velocity[0])
        if(self.angular_velocity[1]):
            self.adjust_yaw(self.angular_velocity[1])
        if(self.angular_velocity[2]):
            self.adjust_roll(self.angular_velocity[2])
        # Apply translations
        self.position = vector_addition(self.position, self.velocity)
        # Decay fine_control_display
        _x = self.fine_control_display[0]
        _y = self.fine_control_display[1]
        _z = self.fine_control_display[2]
        self.fine_control_display[0] = math.copysign(min(3, max(0, abs(_x)-0.2)), _x)
        self.fine_control_display[1] = math.copysign(min(3, max(0, abs(_y)-0.2)), _y)
        self.fine_control_display[2] = math.copysign(min(3, max(0, abs(_z)-0.2)), _z)

    def feel_gravity(self, particle, time_interval):
        if(not self.mass or self is particle):
            return
        # Fgrav = G * ( (m1*m2) / (r**2) )
        # F = ma
        # a = v/t
        f_grav = GRAVITATIONAL_CONSTANT * (
            (self.mass*particle.mass) /
            (distance(self.position, particle.position)**2)
        )
        A = f_grav/self.mass
        V = A * time_interval
        V = scale_vector(unit_vector(vector_between(self.position, particle.position)), V)
        self.velocity = vector_addition(self.velocity, V)
        # Set gravitational reference
        if(
            not self.gravitational_reference or
            f_grav > self.gravitational_reference[1] or
            self.gravitational_reference[0] == particle
        ):
            self.gravitational_reference = (particle, f_grav)
