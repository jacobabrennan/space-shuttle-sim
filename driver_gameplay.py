

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
    def graphic_sort(self, graphic):
        """Sort graphic drawing order. Used by self.display."""
        return -graphic[1][2]
    
    def display(self, screen):
        """Displays the game state on the screen."""
        # Cancel if no camera is available
        if(self.game.ship is None):
            return
        # Get cosmos data from game
        viewpoint = self.game.ship.position
        bearing = self.game.ship.bearing
        attitude = self.game.ship.attitude
        starboard = vector_product(bearing, attitude)
        particles = self.game.particles
        # Get and sort graphics for all particles
        graphics = []
        for particle in particles:
            # Calculate graphic
            graphic = particle.graphic(viewpoint, bearing, attitude, starboard)
            # Skip if particle is behind viewpoint
            if(graphic is None):
                continue
            # Add to list
            graphics.append(graphic)
        # Sort list by distance, farthest first
        graphics.sort(key=self.graphic_sort)
        # Display all graphics
        for graphic in graphics:
            # Center and scale graphic on screen
            display_x = graphic[1][0]
            display_y = graphic[1][1]*-1
            display_x += SCREEN_PHYSICAL_WIDTH/2
            display_y += SCREEN_PHYSICAL_HEIGHT/2
            display_x *= SCREEN_CHARACTER_WIDTH / SCREEN_PHYSICAL_WIDTH
            display_y *= SCREEN_CHARACTER_HEIGHT / SCREEN_PHYSICAL_HEIGHT
            # Discard graphics outside of screen
            if(
                    display_y >= 24 or
                    display_y < 0 or
                    display_x < 0 or
                    display_x >= 79):
                continue
            # Draw graphic
            screen.addstr(int(display_y), int(display_x), graphic[0])
