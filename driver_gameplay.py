

# = Gameplay Screen ===========================================================
"""
The gameplay screen is in active development and its full behavior hasn't
solidified yet. It lacks proper structure and documentation. Be warned.

The gameplay screen handles display when the player is in the main "spaceship"
gameplay mode. It consists of two sub-drivers, the starfield and cockpit
drivers. The Starfield is responsible for projecting the 3D game world onto the
2D terminal screen, while the Cockpit draws a Heads Up Display (HUD) over it.

Together, these objects are responsible for the majority of the user's
experience with the game.
"""


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

    def command(self, command):
        result = super().command(command)
        if(command is COMMAND_TIME_SCALE_INCREASE):
            self.game.scale_time(self.game.time_scale * 10)
        if(command is COMMAND_TIME_SCALE_DECREASE):
            self.game.scale_time(self.game.time_scale / 10)
        return result


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
        angular_radius = RIGHT - math.acos(min(1, particle.radius/absolute_distance))
        return (polar_coordinates, angular_radius, particle)

    def draw_disc(self, screen, disc):
        # Disc Tuple has form: (polar_coords, angular_radius, particle)
        meters_to_pixels = SCREEN_PIXEL_WIDTH/(SCREEN_PHYSICAL_WIDTH)
        pixel_radius = disc[1]*meters_to_pixels
        pixel_x = math.cos(disc[0][1])*disc[0][0]*meters_to_pixels
        pixel_y = math.sin(disc[0][1])*disc[0][0]*meters_to_pixels
        # Draw point-like disc (Degenerate case 1)
        if(pixel_radius < CHARACTER_WIDTH):
            self.draw_point(screen, pixel_x, pixel_y, pixel_radius, disc[0][2], disc[2])
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

    def draw_point(self, screen, pixel_x, pixel_y, pixel_radius, depth, particle):
        char_x = pixel_x / CHARACTER_WIDTH
        char_y = pixel_y / CHARACTER_HEIGHT
        close = (depth < 2*AU)
        # Calculate apparent magnitude
        brightness = particle.magnitude + 2.5*math.log10( ((depth/PARSEC)/10)**2 )
        #
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
        if(brightness < 2):
            self.draw_sprite(screen, char_x, char_y, sprite, curses.A_BOLD)
        else:
            self.draw_sprite(screen, char_x, char_y, sprite, curses.A_DIM)
        #
        if(particle.label):
            offset = 0
            for char in particle.label:
                self.draw_sprite(screen, char_x+1+offset, char_y+1, char)
                offset += 1

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
                    # if(sprite_sides == 15): draw some texture
                    self.draw_sprite(screen, pos_x, pos_y, sprite, curses.A_BOLD)

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
        ship = self.game.ship
        starboard = vector_product(ship.bearing, ship.attitude)
        axes = (starboard, ship.attitude, ship.bearing)
        # Draw HUD background graphic
        for pos_y in range(len(self.hud)):
            line = self.hud[pos_y]
            for pos_x in range(len(line)):
                character = line[pos_x]
                if(character == ' '):
                    continue
                screen.addstr(pos_y, pos_x, character)
        # Display Thrust Output
        # Thrust Title
        screen.addstr(15, 62, 'Thruster-Output', curses.A_BOLD)
        # Thrust Orientation Output
        for axis in range(3):  # Pitch, Yaw, and Roll. Skip forward thrust
            thrust_value = -ship.thrust_display[axis]
            thrust = '|'
            thrust += '>' * math.ceil(thrust_value)
            for char_pos in range(-1, -4, -1):
                sprite = '<'
                if(char_pos < math.floor(thrust_value)):
                    sprite = ' '
                thrust = sprite + thrust
            thrust += ' '*(7-len(thrust))
            screen.addstr(16+axis, 71, thrust, curses.A_BOLD)
        # Thrust Main Thruster Output
        t_width = ship.main_thruster_output / SHUTTLE_THRUST_MAX
        sprite = '«'
        if(t_width < 0):
            sprite = '»'
            t_width = abs(t_width)
        thrust_string = sprite * math.ceil(t_width*12)
        thrust_string = ' '*(12-len(thrust_string))+thrust_string+':'
        screen.addstr(16, 58, thrust_string, curses.A_BOLD)
        thrust_string = sprite * math.ceil(t_width*13)
        thrust_string = ' '*(13-len(thrust_string))+thrust_string+':'
        screen.addstr(17, 57, thrust_string, curses.A_BOLD)
        screen.addstr(19, 61, '  Bearing ', curses.A_BOLD)
        velocity_vector = transform_coordinate_system(
            ship.velocity, (0, 0, 0), axes,
        )
        velocity_magnitude = magnitude(velocity_vector)
        if(velocity_magnitude):
            relative_bearing_vector = unit_vector(velocity_vector)
            azimuth = math.atan2(velocity_vector[0], velocity_vector[2]) * 180/math.pi
            altitude = math.asin(relative_bearing_vector[1]) * 180/math.pi
        else:
            azimuth = 0
            altitude = 0
        display_string = F'  {int(azimuth)}° {int(altitude)}°'
        display_string += ' '*(17-len(display_string))
        screen.addstr(20, 61, display_string, curses.A_BOLD)
        if(velocity_magnitude <= 1):
            velocity_magnitude = 0
        display_string = ' {:.3e} km/s'.format(velocity_magnitude/KILO)
        display_string += ' '*(16-len(display_string))
        screen.addstr(21, 62, display_string, curses.A_BOLD)
        # Display Gravitational Reference Info
        screen.addstr(15, 3, 'Reference-Frame', curses.A_BOLD)
        if(not ship.gravitational_reference):
            return
        reference_point = ship.gravitational_reference[0]
        reference_vector = transform_coordinate_system(
            reference_point.position,
            ship.position,
            axes,
        )
        # G.Ref. Name
        reference_name = ' '+(reference_point.label or "Unknown Body")
        reference_name += ' '*(20-len(reference_name))
        screen.addstr(16, 2, reference_name, curses.A_BOLD)
        # G.Ref. Distance
        reference_distance = magnitude(reference_vector) - reference_point.radius
        if(reference_distance >= AU*10000):
            reference_distance /= LY
            display_string = ' D: {:.3f} ly'.format(reference_distance)
        elif(reference_distance >= AU):
            reference_distance /= AU
            display_string = ' D: {:.3f} au'.format(reference_distance)
        else:
            reference_distance /= 1000
            display_string = ' D: {:.3e} km'.format(reference_distance)
        display_string += ' '*(22-len(display_string))
        screen.addstr(18, 2, display_string, curses.A_BOLD)
        # G.Ref. Azimuth and Altitude (vector to reference)
        if(reference_distance):
            reference_vector = unit_vector(reference_vector)
            azimuth = math.atan2(reference_vector[0], reference_vector[2]) * 180/math.pi
            altitude = math.asin(reference_vector[1]) * 180/math.pi
        else:
            azimuth = 0
            altitude = 0
        display_string = F' V: {int(azimuth)}° {int(altitude)}°'
        display_string += ' '*(21-len(display_string))
        screen.addstr(17, 2, display_string, curses.A_BOLD)
        # Display Mission Time and Time Scale factor
        display_string = F' Time ×{math.ceil(self.game.time_scale)}'.ljust(15)
        screen.addstr(20, 4, display_string, curses.A_BOLD)
        time_components = self.game.time
        if(self.game.time_scale <= 10000):
            seconds = time_components % MINUTE
            time_components -= seconds
            seconds = int(seconds/SECOND)
            minutes = time_components % HOUR
            time_components -= minutes
            minutes = int(minutes/MINUTE)
            hours = time_components % DAY
            time_components -= hours
            hours = int(hours/HOUR)
            days = time_components % YEAR
            time_components -= days
            days = int(days/DAY)
            display_string = ' {:03d}, {:02d}:{:02d}:{:02d}'
            display_string = display_string.format(days, hours, minutes, seconds)
            display_string = display_string.ljust(15)
            screen.addstr(21, 4, display_string, curses.A_BOLD)
        else:
            days = time_components % YEAR
            time_components -= days
            days = int(days/DAY)
            years = int(time_components/YEAR)
            display_string = F' {years}, {days:03d}'.ljust(15)
            screen.addstr(21, 4, display_string, curses.A_BOLD)

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
        ' +-------------------x     \                        /     x-------------------+ ',
        ' |                    \     \______________________/     /                    | ',
        ' |                     \                                /                     | ',
        ' |                      \                               \______________       | ',
        ' |______________________/                                   /          \______| ',
        '   |               \                                        \                 | ',
        '   |               /                                         \                | ',
        '   |______________/                                           \_______________| ',
        '                                                                                ',
    ]
