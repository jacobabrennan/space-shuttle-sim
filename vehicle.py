

# = Vehicle ===================================================================
"""
Vehicles represent dynamic manmade game objects, contrasting with the static
spherical objects in the cosmos. The player's avatar in the game is a basic
vehicle, which they can move around and point in any direction. In the future,
more vehicle types may be added, such as the ISS. This would allowing the
player to view other vehicles while in "space travel" mode, as well as possibly
changing vehicles or game modes entirely.

The directions of "Forward" and "Up" on the user's screen correspond with the
vehicles "bearing" and "attitude" vectors.
"""


# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules
from config import *
from vector3d import *
from particle import Particle
import game


# - Definition and Initialization ----------------
class Vehicle(Particle):
    """
    A vehicle which can change its position, and orientation through all three
    dimensions, velocity, and angular velocity. Vehicles experience the
    gravitational attraction of massive object. Vehicles can be controlled by
    player commands, via the player_control method.
    """

    def __init__(self, position=(0, 0, 0)):
        super().__init__(position)
        # By default, the vehicle is stationary, facing forward, and upright.
        self.velocity = (0, 0, 0)
        self.angular_velocity = (0, 0, 0)  # Radians per tick
        self.bearing = (0, 0, 1)
        self.attitude = (0, 1, 0)
        self.radius = -1  # Quirk so ship is "behind" viewpoint.
        self.gravitational_reference = None
        self.thrust_display = [0, 0, 0]
        self.main_thruster_output = 0
        self.stabilizing = False
        self.game = game.get_game()
        self.game.vehicles.append(self)

    # - Player Controls ------------------------------
    def player_control(self, command):
        """Exposes control of the ship's state to player commands."""
        R = SHIP_TURNING_ANGLE
        if(command is None):
            return
        if(command & COMMAND_UP):
            self.stabilizing = False
            self.pitch(-R)
        if(command & COMMAND_DOWN):
            self.stabilizing = False
            self.pitch(R)
        if(command & COMMAND_LEFT):
            self.stabilizing = False
            self.yaw(R)
        if(command & COMMAND_RIGHT):
            self.stabilizing = False
            self.yaw(-R)
        if(command & COMMAND_ROLL_ANTICLOCK):
            self.stabilizing = False
            self.roll(R)
        if(command & COMMAND_ROLL_CLOCKWISE):
            self.stabilizing = False
            self.roll(-R)
        if(command & COMMAND_FORWARD):
            self.stabilizing = False
            thrust_change = SHUTTLE_THRUST_MAX/10
            if(abs(self.main_thruster_output) < thrust_change):
                self.main_thruster_output = 0
            self.increase_thrust(thrust_change)
        if(command & COMMAND_BACK):
            self.stabilizing = False
            thrust_change = SHUTTLE_THRUST_MAX/10
            if(abs(self.main_thruster_output) < thrust_change):
                self.main_thruster_output = 0
            self.increase_thrust(-thrust_change)
        if(command & COMMAND_STABILIZE):
            self.stabilizing = True

    # - Thrust Controls ------------------------------
    def increase_thrust(self, force):
        """Adjusts the current (ongoing) output of the main thrusters."""
        self.main_thruster_output += force
        if(abs(self.main_thruster_output) > SHUTTLE_THRUST_MAX):
            self.main_thruster_output = math.copysign(
                SHUTTLE_THRUST_MAX,
                self.main_thruster_output,
            )

    def pitch(self, radians):
        """Adjusts angular velocity about the X/lateral axis."""
        if(not radians):
            return
        # Snap to 0 if thrusting opposite spin near 0
        current_vel = self.angular_velocity[0]
        if current_vel * radians < 0:
            if abs(current_vel) < abs(radians):
                radians = -current_vel
        #
        self.angular_velocity = (
            self.angular_velocity[0]+radians,
            self.angular_velocity[1],
            self.angular_velocity[2],
        )
        self.thrust_display[0] += radians/SHIP_TURNING_ANGLE

    def yaw(self, radians):
        """Adjusts angular velocity about the Y/vertical axis."""
        if(not radians):
            return
        # Snap to 0 if thrusting opposite spin near 0
        current_vel = self.angular_velocity[1]
        if current_vel * radians < 0:
            if abs(current_vel) < abs(radians):
                radians = -current_vel
        #
        self.angular_velocity = (
            self.angular_velocity[0],
            self.angular_velocity[1]+radians,
            self.angular_velocity[2],
        )
        self.thrust_display[1] += radians/SHIP_TURNING_ANGLE

    def roll(self, radians):
        """Adjusts angular velocity about the Z/forward axis."""
        if(not radians):
            return
        # Snap to 0 if thrusting opposite spin near 0
        current_vel = self.angular_velocity[2]
        if current_vel * radians < 0:
            if abs(current_vel) < abs(radians):
                radians = -current_vel
        #
        self.angular_velocity = (
            self.angular_velocity[0],
            self.angular_velocity[1],
            self.angular_velocity[2]+radians,
        )
        self.thrust_display[2] += radians/SHIP_TURNING_ANGLE

    def stabilize(self):
        """
        Stabilizes vehicle by brining velocity and angular velocity to Zero.
        """
        # Turn off main thruster (stop increasing velocity)
        self.main_thruster_output = 0
        # Stabilize angular velocity
        thrust = [0, 0, 0, 0]
        _x = self.angular_velocity[0]
        _y = self.angular_velocity[1]
        _z = self.angular_velocity[2]
        stable = True
        if(abs(_x) < SHIP_TURNING_ANGLE):
            _x = 0
        else:
            stable = False
            thrust[0] = (-_x)*0.5
        if(abs(_y) < SHIP_TURNING_ANGLE):
            _y = 0
        else:
            stable = False
            thrust[1] = -(_y)*0.5
        if(abs(_x) < SHIP_TURNING_ANGLE):
            _z = 0
        else:
            stable = False
            thrust[2] = -_z/2
        if(stable):
            self.stabilizing = False
        self.angular_velocity = (_x, _y, _z)
        self.pitch(thrust[0])
        self.yaw(thrust[1])
        self.roll(thrust[2])
        # Halt movement completely.
        # This is a cheat, but the game is unplayable otherwise.
        self.velocity = (0, 0, 0)

    def adjust_pitch(self, radians):
        """Adjusts bearing & attitude by rotating about the X/lateral axis."""
        new_bearing = vector_addition(
            scale_vector(self.bearing, math.cos(radians)),
            scale_vector(self.attitude, math.sin(radians)),
        )
        self.attitude = vector_addition(
            scale_vector(self.bearing, math.cos(radians+RIGHT)),
            scale_vector(self.attitude, math.sin(radians+RIGHT)),
        )
        self.bearing = new_bearing

    def adjust_yaw(self, radians):
        """Adjusts bearing & attitude by rotating about the Y/vertical axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.bearing = vector_addition(
            scale_vector(starboard, math.cos(radians+RIGHT)),
            scale_vector(self.bearing, math.sin(radians+RIGHT)),
        )

    def adjust_roll(self, radians):
        """Adjusts bearing & attitude by rotating about the Z/forward axis."""
        starboard = vector_product(self.bearing, self.attitude)
        self.attitude = vector_addition(
            scale_vector(starboard, math.cos(radians+RIGHT)),
            scale_vector(self.attitude, math.sin(radians+RIGHT)),
        )

    # - Behavior Over Time ---------------------------
    def take_turn(self, time_interval):
        """Determines how the vehicle behaves every game loop iteration."""
        # Stabilize
        if(self.stabilizing):
            self.stabilize()
        # Apply Thrust
        if(self.main_thruster_output):
            f_thrust = scale_vector(self.bearing, self.main_thruster_output)
            self.apply_force(f_thrust, time_interval)
            # self.thrust(self.main_thruster_output, time_interval)
        # Apply rotations
        if(self.angular_velocity[0]):
            self.adjust_pitch(self.angular_velocity[0])
        if(self.angular_velocity[1]):
            self.adjust_yaw(self.angular_velocity[1])
        if(self.angular_velocity[2]):
            self.adjust_roll(self.angular_velocity[2])
        # Apply translations
        scaled_velocity = scale_vector(self.velocity, time_interval)
        self.position = vector_addition(self.position, scaled_velocity)
        # Decay thrust_display
        _x = self.thrust_display[0]
        _y = self.thrust_display[1]
        _z = self.thrust_display[2]
        self.thrust_display[0] = math.copysign(min(3, max(0, abs(_x)-0.2)), _x)
        self.thrust_display[1] = math.copysign(min(3, max(0, abs(_y)-0.2)), _y)
        self.thrust_display[2] = math.copysign(min(3, max(0, abs(_z)-0.2)), _z)

    # - Gravity --------------------------------------
    def apply_force(self, force_vector, time_interval):
        """Applies a force in newtons over a time interval in seconds."""
        # F = MA
        # A = V/T
        V = scale_vector(force_vector, time_interval/self.mass)
        self.velocity = vector_addition(self.velocity, V)

    def feel_gravity(self, particle, time_interval):
        """Applies gravitational force to the vehicle over the given time."""
        # If either particle has no mass, do nothing
        if(not self.mass or self is particle):
            return
        # Calculate the force of gravity as a vector
        # Note: f_grav = G * ( (m1*m2) / (r**2) )
        delta_position = vector_between(self.position, particle.position)
        distance = magnitude(delta_position)
        f_grav = GRAVITATIONAL_CONSTANT * (
            (self.mass*particle.mass) /
            (distance**2)
        )
        force_vector = scale_vector(unit_vector(delta_position), f_grav)
        self.apply_force(force_vector, time_interval)
        # Set gravitational reference
        if(
            not self.gravitational_reference or
            f_grav > self.gravitational_reference[1] or
            self.gravitational_reference[0] == particle
        ):
            self.gravitational_reference = (particle, f_grav)
