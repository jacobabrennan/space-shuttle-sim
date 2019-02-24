

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
        self.starfield = Starfield()
        self.cockpit = Cockpit()

    def display(self, screen):
        """Displays the game state on the screen."""
        # Cancel if no camera is available
        if(self.game.ship is None):
            return
        self.starfield.display(screen)
        self.cockpit.display(screen)


# = Starfield Screen Definition ===============================================

# - Initialization -------------------------------
class Starfield(Driver):
    def __init__(self):
        super().__init__()
        self.game = game.get_game()

    # - Interaction ----------------------------------

    # - Display Functions ----------------------------
    def display(self, screen):
        # Get cosmos data from game
        viewpoint = self.game.ship.position
        bearing = self.game.ship.bearing
        attitude = self.game.ship.attitude
        starboard = vector_product(bearing, attitude)
        particles = self.game.particles.copy()
        particles.remove(self.game.ship)
        axes = (starboard, attitude, bearing)
        # Get display discs for each particle in view, sorted by depth
        display_discs = []
        for particle in particles:
            # Determine particle position relative to viewport and axes
            relative_position = transform_coordinate_system(
                particle.position, viewpoint, axes)
            # Disregard objects that are fully behind the viewpoint
            # if(relative_position[2] == 0):
            #     continue
            # Calculate display disc
            display_discs.append(self.scale_display_disc(
                relative_position, particle
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

    def scale_display_disc(self, relative_position, particle):
        """Calculates the disc on which to draw a particle."""
        # Determine position on screen, based on view angle
        # View screen is a roughly rectangular section of a larger sphere
        # Find polar coordinates of relative direction projected onto surface
        absolute_distance = magnitude(relative_position)
        polar_coordinates = (
            math.acos(relative_position[2]/absolute_distance),
            math.atan2(relative_position[1], relative_position[0]),
            absolute_distance,
        )
        angular_radius = math.pi/2 - math.acos(min(1,particle.radius/absolute_distance))
        return (polar_coordinates, angular_radius, particle)

    def draw_disc(self, screen, disc):
        # Disc Tuple has form: (polar_coords, angular_radius, particle)
        meters_to_pixels = SCREEN_PIXEL_WIDTH/(SCREEN_PHYSICAL_WIDTH/2)
        pixel_radius = disc[1]*meters_to_pixels
        pixel_x = math.cos(disc[0][1])*disc[0][0]*meters_to_pixels
        pixel_y = math.sin(disc[0][1])*disc[0][0]*meters_to_pixels
        # Draw point-like disc (Degenerate case 1)
        if(pixel_radius < CHARACTER_WIDTH):
            self.draw_point(screen, pixel_x, pixel_y, pixel_radius, disc[0][2])
            return
        # Draw planet surface (Degenerate case 2)
        if(disc[0][0] > math.pi):
            # Isn't actually happening
            pass
        # Draw large circle (Regular disc)
        # Distortion is used to simulate rotated ellipses at the edges of the
        # view area. This allows for views of a planet's surface / horizon.
        distortion = abs(1/math.cos(disc[0][0]))
        distortion_radius = (distortion-1) * pixel_radius
        pixel_x += math.cos(disc[0][1]) * distortion_radius
        pixel_y += math.sin(disc[0][1]) * distortion_radius
        pixel_radius += distortion_radius
        self.draw_circle(screen, pixel_x, pixel_y, pixel_radius)

    def sort_display_discs(self, disc):
        """Sort drawing order by depth. Used by self.display."""
        return -(disc[0][2])

    def draw_point(self, screen, pixel_x, pixel_y, pixel_radius, depth):
        char_x = pixel_x / CHARACTER_WIDTH
        char_y = pixel_y / CHARACTER_HEIGHT
        close = (depth < 1/2*AU)
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

    def draw_circle(self, screen, pixel_x, pixel_y, pixel_radius):
        # Get edges of disc bounding rectangle
        # Start at pixel precision
        left_edge = (pixel_x - pixel_radius)
        right_edge = (left_edge + pixel_radius*2)
        bottom_edge = (pixel_y - pixel_radius)
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
        disc_center = (pixel_x, pixel_y, 0)
        for pos_y in range(bottom_edge, top_edge+1):
            for pos_x in range(left_edge, right_edge+1):
                # To determine if a full or partial space should be drawn:
                # Get central vector
                center = (
                    (pos_x)*CHARACTER_WIDTH,
                    (pos_y)*CHARACTER_HEIGHT,
                    0,  # z coords match, in same plane
                )
                # Compare to sides of character space rectangle
                dist_left = distance(
                    disc_center,
                    (center[0]-CHARACTER_WIDTH/2, center[1], center[2]),
                )
                dist_right = distance(
                    disc_center,
                    (center[0]+CHARACTER_WIDTH/2, center[1], center[2]),
                )
                dist_bottom = distance(
                    disc_center,
                    (center[0], center[1]-CHARACTER_HEIGHT/2, center[2]),
                )
                dist_top = distance(
                    disc_center,
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

    sprite_sides = [
        '@', '"', '_', '+',
        '(', '\\', '/', '[',
        ')', '/', '\\', ']',
        '+', '%', '"', '#',
    ]


# = Cockpit HUD Definition ====================================================

# - Initialization -------------------------------
class Cockpit(Driver):
    def __init__(self):
        super().__init__()
        self.game = game.get_game()

    # - Interaction ----------------------------------

    # - Display Functions ----------------------------
    def display(self, screen):
        # Draw HUD background graphic
        for pos_y in range(len(self.hud)):
            line = self.hud[pos_y]
            for pos_x in range(len(line)):
                character = line[pos_x]
                if(character is ' '):
                    continue
                screen.addstr(pos_y, pos_x, character)
        # Display Vector (bearing)
        # pos_x = int(self.game.ship.bearing[0]*100)
        # pos_y = int(self.game.ship.bearing[1]*100)
        # pos_z = int(self.game.ship.bearing[2]*100)
        # display_string = F' V: <{pos_x}, {pos_y}, {pos_z}>'
        # display_string += ' '*(20-len(display_string))
        # screen.addstr(19, 2, display_string, curses.A_BOLD)
        # Display Vector to Earth
        earth_vector = transform_coordinate_system(
            self.game.earth.position,
            self.game.ship.position,
            (
                vector_product(self.game.ship.bearing, self.game.ship.attitude),
                self.game.ship.attitude,
                self.game.ship.bearing,
            )
        )
        #
        earth_distance = magnitude(earth_vector) - self.game.earth.radius
        display_string = F' D: {int(earth_distance)}'
        display_string += ' '*(21-len(display_string))
        screen.addstr(20, 2, display_string, curses.A_BOLD)
        #
        earth_vector = unit_vector(earth_vector)
        azimuth = int(math.atan2(earth_vector[0], earth_vector[2]) * 180/math.pi)
        altitude = int(math.asin(earth_vector[1]) * 180/math.pi)
        display_string = F' E: <{azimuth}, {altitude}>'
        display_string += ' '*(20-len(display_string))
        screen.addstr(19, 2, display_string, curses.A_BOLD)
        # Display Mission Time (days passed)
        display_string = F' T: {int((self.game.time*TICK_SECONDS)/(60*60*24))} days'
        display_string += ' '*(22-len(display_string))
        screen.addstr(21, 2, display_string, curses.A_BOLD)

        display_string += ' '*(21-len(display_string))
    # - HUD Graphic ----------------------------------
    hud = [
        '       /                                                                \       ',
        '      /                                                                  \      ',
        '     /                                                                    \     ',
        '    /                                                                      \    ',
        '___/\                                                                      /\___',
        '   \ \                                                                    / /   ',
        '    \ \                                                                  / /    ',
        '     \ \                                                                / /     ',
        '      \ \                                                              / /      ',
        '       \ \                                                            / /       ',
        '        \ \                                                          / /        ',
        '         \ \                                                        / /         ',
        '          \ \                                                      / /          ',
        '           \ \          \                              /          / /           ',
        '------------\-------------\                          /-------------/------------',
        '             \             \                        /             /             ',
        '              \             \______________________/             /              ',
        '               \                                                /               ',
        ' +-------------------x                                    x-------------------+ ',
        ' |                    \                                  /                    | ',
        ' |                     \                                /                     | ',
        ' |                      \                              /                      | ',
        ' |______________________/                              \______________________| ',
        '                  /                                          \                  ',
    ]