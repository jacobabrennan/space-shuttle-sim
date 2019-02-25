

# = Game Singleton ============================================================

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
    global game
    # Generate a game if necessary
    if(game is None):
        game = Game(*args)
    # Return the game
    return game


# - Game Object ----------------------------------
class Game:
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
        if(self.time is None):
            return
        self.time += 1
        # Handle ship controls (player commands)
        S = self.ship
        R = SHIP_TURNING_ANGLE
        accelleration = 100
        if(player_command == COMMAND_UP):
            S.pitch(-R)
        elif(player_command == COMMAND_DOWN):
            S.pitch(R)
        elif(player_command == COMMAND_LEFT):
            S.yaw(R)
        elif(player_command == COMMAND_RIGHT):
            S.yaw(-R)
        elif(player_command == COMMAND_ROLL_ANTICLOCK):
            S.roll(R)
        elif(player_command == COMMAND_ROLL_CLOCKWISE):
            S.roll(-R)
        elif(player_command == COMMAND_FORWARD):
            S.increase_thrust(1000*S.mass)
        elif(player_command == COMMAND_BACK):
            S.increase_thrust(-1000*S.mass)
        # Move all particles
        for particle in self.particles:
            particle.take_turn(self.time)
            if(particle.mass):
                for vehicle in self.vehicles:
                    vehicle.feel_gravity(particle, TICK_SECONDS)

    def start(self):
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
        new_particle = Particle((pos_x*57909050*KILO, 0, pos_y*57909050*KILO), 2439.7*KILO, mass=3.3011e+23)
        self.particles.append(new_particle)
        new_particle.label = 'Mercury'
        # Venus
        pass
        # Earth
        new_particle = Particle((AU, 0, (384399*KILO)/2), 6371*KILO, mass=5.972e+24)
        self.particles.append(new_particle)
        self.earth = new_particle
        new_particle.label = 'Earth'
        # Moon
        new_particle = Particle((AU, 0, -(384399*KILO)/2), 1737.1*KILO, mass=7.342e+22)
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
