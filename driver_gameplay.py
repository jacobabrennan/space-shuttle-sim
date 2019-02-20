

# = Gameplay Screen ===========================================================

# - Dependencies ---------------------------------
# Python Modules
import random
# Local Modules
from config import *
from vector3d import *
from driver import Driver
import game


# = Gameplay Screen Definition ================================================

# - Initialization -------------------------------
class Gameplay(Driver):
    def __init__(self):
        super().__init__()
        self.game = game.get_game()

    # - Interaction ----------------------------------

    # - Display Functions ----------------------------
    def display(self, screen):
        screen.addstr(0, 0, "Gameplay Screen")
        # screen.addstr(11, 28, F'Random Integer: {random.randint(1000,9999)}')
        # screen.addstr(13, 28, F'Last Client Command: {command}')
        #
        if(self.game.ship is None):
            return
        #
        viewpoint = self.game.ship.position
        bearing = self.game.ship.bearing
        attitude = self.game.ship.attitude
        starboard = vector_product(bearing, attitude)
        # Show all particles
        particles = self.game.particles
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for particle in particles:
            graphic = particle.graphic(viewpoint, bearing, attitude, starboard)
            if(graphic is None):
                continue
            display_x = graphic[1][0]
            display_y = graphic[1][1]*-1
            display_x += SCREEN_PHYSICAL_WIDTH/2
            display_y += SCREEN_PHYSICAL_HEIGHT/2
            display_x *= SCREEN_CHARACTER_WIDTH / SCREEN_PHYSICAL_WIDTH
            display_y *= SCREEN_CHARACTER_HEIGHT / SCREEN_PHYSICAL_HEIGHT
            #
            if(min_x is None or min_x > display_x):
                min_x = display_x
            if(max_x is None or max_x < display_x):
                max_x = display_x
            if(min_y is None or min_y > display_y):
                min_y = display_y
            if(max_y is None or max_y < display_y):
                max_y = display_y
            if(
                    display_y >= 24 or
                    display_y < 0 or
                    display_x < 0 or
                    display_x >= 79):
                continue
            screen.addstr(int(display_y), int(display_x), graphic[0])
