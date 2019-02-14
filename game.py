

# = Game Singleton ============================================================

# - Dependencies ---------------------------------
# Python Modules
import threading
import array
# Local Modules
from config import *

# - Game access function -------------------------
game = None


def get_game():
    global game
    # Generate a game if necessary
    if(game is None):
        game = Game()
    # Return the game
    return game


# - Game Object ----------------------------------
class Game:
    def __init__(self):
        super().__init__()
        self.time = None

    def iterate(self, player_command):
        if(self.time is not None):
            self.time += 1

    def start(self):
        self.time = 0
        # Populate map as a grid of tile ids
        self.tile_grid = array.array('B')
        for index in range(0, (SCREEN_SIZE_HEIGHT * SCREEN_SIZE_WIDTH)-1):
            self.tile_grid.append(0)
        # for posY = 0 to SCREEN_SIZE_HEIGHT-1:
        #     for posX = 0 to SCREEN_SIZE_WIDTH-1:
        #         compound_index = posY*SCREEN_SIZE_WIDTH + posX
        #         tile
            
        this.map.length
