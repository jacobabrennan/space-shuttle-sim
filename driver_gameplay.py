

# = Gameplay Screen ===========================================================

# - Dependencies ---------------------------------
# Python Modules
import random
import curses
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
        axes = (starboard, attitude, bearing)
        # Get display discs for each particle in view, sorted by depth
        display_discs = []
        for particle in particles:
            # Determine particle position relative to viewport and axes
            relative_position = transform_coordinate_system(
                particle.position, viewpoint, axes)
            depth = relative_position[2]
            # Disregard objects that are fully behind the viewpoint
            if(depth <= -particle.radius):
                continue
            # Calculate display disc
            display_discs.append(self.scale_display_disc(
                particle.radius, relative_position, particle
            ))
        display_discs.sort(key=self.sort_display_discs)
        # Draw particles onto discs
        for disc in display_discs:
            self.draw_disc(screen, disc)

    def draw_sprite(self, screen, char_x, char_y, sprite, style=curses.A_NORMAL):
        """Draws a single character at a Character position on the screen."""
        # Center graphic on screen
        screen_x = int(SCREEN_CHARACTER_WIDTH/2 + char_x)
        screen_y = int(SCREEN_CHARACTER_HEIGHT/2 - char_y)
        # Discard graphics outside of screen
        if(
            screen_y >= SCREEN_CHARACTER_HEIGHT or
            screen_y < 0 or
            screen_x < 0 or
            screen_x >= SCREEN_CHARACTER_WIDTH or
            (  # Curses can't draw to lower right corner
                screen_x == SCREEN_CHARACTER_WIDTH-1 and
                screen_y == SCREEN_CHARACTER_HEIGHT-1
            )
        ):
            return
        screen.addstr(screen_y, screen_x, sprite, style)

    def scale_display_disc(self, radius, relative_position, particle):
        """Calculates the disc on which to draw a particle."""
        # Determine display size with depth scaling
        depth = relative_position[2]
        if(depth >= 0):
            scale = 1 / max(1, depth)
        else:
            scale = 1 / abs(min(-1, depth))
        # Determine pixel measurements of radius and position
        meters_to_pixels = SCREEN_PIXEL_WIDTH/SCREEN_PHYSICAL_WIDTH
        pixel_position = (  # Offset from origin, in terms of pixels
            relative_position[0]*scale*meters_to_pixels,
            relative_position[1]*scale*meters_to_pixels,
            depth,
        )
        pixel_radius = radius * scale * meters_to_pixels
        return (pixel_position, pixel_radius, particle)

    def draw_disc(self, screen, disc):
        # Disc Tuple has form: (position, radius)
        pixel_radius = disc[1]
        # Draw point-like disc
        if(pixel_radius < CHARACTER_WIDTH):
            char_x = disc[0][0] / CHARACTER_WIDTH
            char_y = disc[0][1] / CHARACTER_HEIGHT
            close = (disc[0][2] < 10*AU)
            sprite = '·'
            if(pixel_radius < 1):
                sprite = '·'
                if(close and random.random() < 1/8):
                    sprite = random.choice(('+', '×'))
            elif(pixel_radius < 4):
                sprite = '•'
            elif(pixel_radius < 5):
                sprite = 'o'
            else:
                sprite = '@'
                # °*+@Oo©®
            #
            if(close):
                self.draw_sprite(screen, char_x, char_y, sprite, curses.A_BOLD)
            else:
                self.draw_sprite(screen, char_x, char_y, sprite, curses.A_DIM)
            return
        # Get edges of disc bounding rectangle
        # Start at pixel precision
        left_edge = (disc[0][0] - pixel_radius)
        right_edge = (left_edge + pixel_radius*2)
        bottom_edge = (disc[0][1] - pixel_radius)
        top_edge = (bottom_edge + pixel_radius*2)
        # Resolve pixel values to character precision
        left_edge /= CHARACTER_WIDTH
        right_edge /= CHARACTER_WIDTH
        bottom_edge /= CHARACTER_HEIGHT
        top_edge /= CHARACTER_HEIGHT
        # Cancel drawing if disc is entirely outside the screen
        if(
            right_edge < int(-SCREEN_CHARACTER_WIDTH/2) or
            left_edge >= int(SCREEN_CHARACTER_WIDTH/2) or
            top_edge < int(-SCREEN_CHARACTER_HEIGHT/2) or
            bottom_edge >= int(SCREEN_CHARACTER_HEIGHT/2)
        ):
            return
        # Get intersection of bounding rectangle and screen
        left_edge = int(max(left_edge, -SCREEN_CHARACTER_WIDTH/2))
        right_edge = int(min(right_edge, SCREEN_CHARACTER_WIDTH/2))
        bottom_edge = int(max(bottom_edge, -SCREEN_CHARACTER_HEIGHT/2))
        top_edge = int(min(top_edge, SCREEN_CHARACTER_HEIGHT/2))
        # Draw each character space within the display disc
        for pos_y in range(bottom_edge, top_edge+1):
            for pos_x in range(left_edge, right_edge+1):
                # To determine if a full or partial space should be drawn:
                # Get central vector
                center = (
                    (pos_x)*CHARACTER_WIDTH,
                    (pos_y)*CHARACTER_HEIGHT,
                    disc[0][2],  # z coords match, in same plane
                )
                # Compare to sides of character space rectangle
                dist_left = distance(
                    disc[0],
                    (center[0]-CHARACTER_WIDTH/2, center[1], center[2]),
                )
                dist_right = distance(
                    disc[0],
                    (center[0]+CHARACTER_WIDTH/2, center[1], center[2]),
                )
                dist_bottom = distance(
                    disc[0],
                    (center[0], center[1]-CHARACTER_HEIGHT/2, center[2]),
                )
                dist_top = distance(
                    disc[0],
                    (center[0], center[1]+CHARACTER_HEIGHT/2, center[2]),
                )
                # Determine which sides are within the disc radius
                sprite_sides = 0
                if(dist_left <= pixel_radius):
                    sprite_sides |= 8
                if(dist_right <= pixel_radius):
                    sprite_sides |= 4
                if(dist_bottom <= pixel_radius):
                    sprite_sides |= 2
                if(dist_top <= pixel_radius):
                    sprite_sides |= 1
                # Draw the appropriate character
                if(sprite_sides):
                    sprite = self.sprite_sides[sprite_sides]
                    # if(sprite_sides == 15):
                    #     self.draw_sprite(screen, pos_x, pos_y, sprite, curses.A_REVERSE | curses.A_BOLD)
                    #     # sprite = disc[2].sprite(
                    #     #     pixel_radius,
                    #     #     vector_between(disc[0], center)
                    #     # )
                    self.draw_sprite(screen, pos_x, pos_y, sprite)

    def sort_display_discs(self, disc):
        """Sort drawing order by depth. Used by self.display."""
        return -(disc[0][2])

    sprite_sides = [
        '@', '"', '_', '+',
        '(', '\\', '/', '[',
        ')', '/', '\\', ']',
        '+', '%', 'x', '#',
    ]
