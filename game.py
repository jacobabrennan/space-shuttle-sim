

# = Game Singleton ============================================================
"""
The Game class is a singleton and must be accessed via the get_game function.
The game object handles all game logic and the game loop. It's main purpose is
to create the game world and to call each particle's take_turn method every
game loop iteration.
"""


# - Dependencies ---------------------------------
# Python Modules
import threading
import array
import threading
import math
import time
from random import random
# Local Modules
from config import *
from vector3d import *
import client
from particle import Particle
from vehicle import Vehicle
from cosmos import populate_stars

# - Game access function -------------------------
game = None


def get_game(*args):
    """
    Retrieves the game singleton.
    The Game class should not be instanced directly.
    """
    global game
    # Generate a game if necessary
    if(game is None):
        game = Game(*args)
    # Return the game
    return game


# - Game Object ----------------------------------
class Game:
    """
    The Game class is a singleton and should be accessed via the get_game
    function. The game object manages logic for all gameplay objects, such
    as stars and the player vehicle.
    """

    def __init__(self, screen):
        super().__init__()
        self.time = None
        self.ship = None
        self.time_scale = 1
        # Setup thread for game loop
        the_client = client.get_client()

        def game_loop():
            while(True):
                # Get commands from client
                client_command = the_client.key_command
                the_client.key_clear()
                # Do game logic
                self.iterate(client_command)
                # Draw Display
                the_client.display(screen)
                # Sleep
                time.sleep(TIME_GAME_TICK)

        thread_game = threading.Thread(
            target=game_loop,
            name="Game Loop",
            daemon=True)
        thread_game.start()

    def iterate(self, player_command):
        """
        Executes game behavior for each game loop iteration.
        Its primary functions are to increase game time, route player commands
        to controllable game objects, and instruct each game object to perform
        its own turn taking behavior.
        """
        # Handle time management
        if(self.time is None):
            return
        time_interval = self.time_scale * TIME_GAME_TICK
        self.time += time_interval
        # Handle ship controls (player commands)
        S = self.ship
        S.player_control(player_command)
        # Move all particles
        for particle in self.particles:
            particle.take_turn(time_interval)
            if(particle.mass):
                for vehicle in self.vehicles:
                    vehicle.feel_gravity(particle, time_interval)

    def start(self):
        """
        BANG!
        Generates the Cosmos, the player's vehicle, and all other game objects
        necessary to start the game.
        """
        self.time = 0
        # Populate cosmos
        self.particles = []
        self.vehicles = []
        self.ship = Vehicle()
        self.ship.mass = SHUTTLE_MASS
        self.ship.bearing = (1, 0, 0)
        self.ship.attitude = (0, -math.cos(RIGHT), -math.sin(RIGHT), 0)
        self.ship.position = (AU, 0, 403*KILO+(6371*KILO)+(384399*KILO)/2)
        self.ship.velocity = (7.7*KILO, 0, 0)
        self.ship.angular_velocity = (math.pi/835, 0, 0)  #OK!
        self.particles.append(self.ship)
        self.time_scale = 100
        # self.ship.velocity = (0, 0, 0)#AU/10000)#/KILO)
        # Cosmos
        self.particles.extend(populate_stars())
        # Milky Way
        for I in range(0, 200):
            # 63* inclination of milkyway
            # 200 kly diameter
            theta = random()*math.pi*2
            pos_x = math.cos(theta)
            pos_y = math.sin(theta)
            position = (
                pos_x * random()*200*LY*KILO,
                pos_y * random()*200*LY*KILO,
                (random()-1/2)*25*LY*KILO,
            )
            position = transform_coordinate_system(
                position, (26.4*LY*KILO, 0, 25*LY*KILO),
                (
                    (1, 0, 0),
                    (0, math.sin(math.pi/3), math.cos(math.pi/3)),
                    (0, math.cos(math.pi/3), math.sin(math.pi/3)),
                )
            )
            new_particle = Particle(position, random()*695000*KILO)
            self.particles.append(new_particle)
        # Solar neighborhood
        # for I in range(0, 200):
        #     position = (
        #         (random()-1/2)*200*LY,
        #         (random()-1/2)*200*LY,
        #         (random()-1/2)*200*LY,
        #     )
        #     new_particle = Particle(position, random()*695000*KILO)
        #     self.particles.append(new_particle)
        # Sun
        new_particle = Particle((0, 0, 0), 695000*KILO, mass=1.9885e+30)
        self.particles.append(new_particle)
        new_particle.label = 'Sol'
        # Mercury
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*57909050*KILO, 0, pos_y*57909050*KILO),
            2439.7*KILO,
            mass=3.3011e+23)
        self.particles.append(new_particle)
        new_particle.label = 'Mercury'
        # Venus
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*0.723332*AU, 0, pos_y*0.723332*AU),
            6051.8*KILO,
            mass=4.8675e+24)
        self.particles.append(new_particle)
        new_particle.label = 'Venus'
        # Earth
        new_particle = Particle(
            (AU, 0, (384399*KILO)/2),
            6371*KILO,
            mass=5.972e+24)
        self.particles.append(new_particle)
        self.earth = new_particle
        new_particle.label = 'Earth'
        # Moon
        new_particle = Particle(
            (AU, 0, -(384399*KILO)/2),
            1737.1*KILO,
            mass=7.342e+22)
        self.particles.append(new_particle)
        new_particle.label = 'Luna'
        # Mars
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*1.523679*AU, 0, pos_y*1.523679*AU),
            3389.5*KILO,
            mass=6.4171e+23)
        self.particles.append(new_particle)
        new_particle.label = 'Mars'
        # Asteroid Belt
        # for I in range(0, 200):
        #     theta = random()*math.pi*2
        #     pos_x = math.cos(theta)
        #     pos_y = math.sin(theta)
        #     position = (
        #         pos_x * (2*AU + random()*1*AU),
        #         (random()-1/2) * AU/2,
        #         pos_y * (2*AU + random()*1*AU),
        #     )
        #     new_particle = Particle(position, random()*100*KILO)
        #     self.particles.append(new_particle)
        # Jupiter
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*5.2044*AU, 0, pos_y*5.2044*AU),
            69911*KILO,
            mass=1.8982e+27)
        self.particles.append(new_particle)
        new_particle.label = 'Jupiter'
        # Saturn
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*9.5826*AU, 0, pos_y*9.5826*AU),
            58232*KILO,
            mass=5.6834e+26)
        self.particles.append(new_particle)
        new_particle.label = 'Saturn'
        # Uranus
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*19.2184*AU, 0, pos_y*19.2184*AU),
            25362*KILO,
            mass=8.6810e+25)
        self.particles.append(new_particle)
        new_particle.label = 'Uranus'
        # Neptune
        theta = random()*math.pi*2
        pos_x = math.cos(theta)
        pos_y = math.sin(theta)
        new_particle = Particle(
            (pos_x*30.11*AU, 0, pos_y*30.11*AU),
            24622*KILO,
            mass=1.02413e+26)
        self.particles.append(new_particle)
        new_particle.label = 'Neptune'

    def scale_time(self, time_scale):
        """Set the game's time scale to the specified multiple of real time."""
        # Bound scaling factor between real time and e+6, roughly 1s = 11.5days
        new_time_scale = time_scale
        if(new_time_scale < 1):
            new_time_scale = 1
        elif(new_time_scale > 10000000):
            new_time_scale = 10000000
        self.time_scale = new_time_scale
