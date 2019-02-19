

# = Game Singleton ============================================================

# - Dependencies ---------------------------------
# Python Modules
import threading
import array
import threading
import time
import random
# Local Modules
from config import *
from client import get_client
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
        # Setup thread for game loop
        client = get_client()

        def game_loop():
            while(True):
                # Get commands from client
                client_command = client.key_command
                client.key_clear()
                # Do game logic
                self.iterate(client_command)
                # Draw Display
                client.display(
                    screen,
                    self.ship.position, self.ship.orientation, self.particles,
                )
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
        # Move all particles
        for particle in self.particles:
            particle.take_turn(self.time)

    def start(self):
        self.time = 0
        # Populate map as a grid of tile ids
        # self.tile_grid = array.array('B')
        # for index in range(0, (SCREEN_SIZE_HEIGHT * SCREEN_SIZE_WIDTH)-1):
        #     self.tile_grid.append(0)
        # for posY = 0 to SCREEN_SIZE_HEIGHT-1:
        #     for posX = 0 to SCREEN_SIZE_WIDTH-1:
        #         compound_index = posY*SCREEN_SIZE_WIDTH + posX
        #         tile
        # Populate cosmos
        self.ship = Vehicle()
        self.particles = []
        for I in range(0, 500):
            position = (random()*40*AU, random()*40*AU, random()*40*AU)
            new_particle = Particle(position, random()*10*KILO)
            self.particles.append(new_particle)
        # Create player Spaceship
        self.particles.append()
