

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
        if(self.time is None):
            return
        self.time += 1
        # Handle ship controls (player commands)
        S = self.ship
        S.player_control(player_command)
        # Move all particles
        for particle in self.particles:
            particle.take_turn(self.time)
            if(particle.mass):
                for vehicle in self.vehicles:
                    vehicle.feel_gravity(particle, TICK_SECONDS)

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
        self.ship.mass = 74842
        self.ship.bearing = (0, 0, 1)
        self.ship.position = (AU, 0, 1+(6371*KILO)+(384399*KILO)/2)
        self.particles.append(self.ship)
        # self.ship.velocity = (0, 0, 0)#AU/10000)#/KILO)
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
        for I in range(0, 200):
            position = (
                (random()-1/2)*200*LY,
                (random()-1/2)*200*LY,
                (random()-1/2)*200*LY,
            )
            new_particle = Particle(position, random()*695000*KILO)
            self.particles.append(new_particle)
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
        pass
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
        # Mars
        pass
        # Asteroid Belt
        # for I in range(0, 200):
        #     theta = random()*math.pi*2
        #     pos_x = math.cos(theta)
        #     pos_y = math.sin(theta)
        #     position = (
        #         pos_x * 2*AU + random()*1*AU,
        #         (random()-1/2) * AU/2,
        #         pos_y * 2*AU + random()*1*AU,
        #     )
        #     new_particle = Particle(position, random()*100*KILO)
        #     self.particles.append(new_particle)
