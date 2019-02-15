

# = Title Screen ==============================================================

# - Dependencies ---------------------------------
# Python Modules
import curses
import random
# Local Modules
from config import *
from driver import Driver
import client
from driver_gameplay import Gameplay


class Title(Driver):

    # - Initialization -------------------------------
    def __init__(self):
        super().__init__()
        self.star_field()
        self.graphic = False

    # - Interaction ----------------------------------
    def command(self, which):
        # Check for blocking children
        block = super().command(which)
        if(block):
            return block
        # Handle Start Game
        if(which is COMMAND_PRIMARY):
            self.new_game()

    def new_game(self):
        the_client = client.get_client()
        the_client.focus(Gameplay())

    # - Display --------------------------------------
    def display(self, screen, **options):
        # Check for blocking children
        block = super().display(screen, **options)
        if(block):
            return block
        # Display Animated Star Field
        self.star_advance(screen)
        #
        window_height = 24
        window_width = 80
        game_title = "Space Game"
        game_title_graphic = [
            "    ___                   __              ",
            "  ,' _/ _   _   __  __  ,'_/  _   _     __",
            " _\ `. /o|,'o|,',','o/ / /_n,'o| / \\'\,'o/",
            "/___,'/_,'|_,7\_\ |_(  |__,'|_,7/_nn_/|_( ",
            "     //                                   ",
        ]
        press_space = "Press Space to Start"
        screen.addstr(0, 0, game_title)
        line_pos = 8
        for line in game_title_graphic:
            screen.addstr(line_pos, 20, line, curses.A_BOLD)
            line_pos += 1
        screen.addstr(
            line_pos+1,
            int((window_width-len(press_space))/2),
            press_space)
        #
        return True

    class Star:
        def __init__(self):
            self.x = random.random()
            self.y = random.random()
            self.z = 0

    def star_field(self):
        self.stars = []
        for index in range(1, 100):
            new_star = self.Star()
            new_star.z = random.randint(0, 20*7)
            self.stars.append(new_star)

    def star_advance(self, screen):
        old_stars = list(self.stars)
        for star in old_stars:
            star.z += 1
            display_z = star.z / 20
            display_x = star.x - 0.5
            display_x *= 40 + (display_z**2)*40
            display_x = int(display_x + 40)
            display_y = star.y - 0.5
            display_y *= 12 + (display_z**2)*12
            display_y = int(display_y + 12)
            if(
                    # display_z >= 1 or
                    display_y >= 24 or
                    display_y < 0 or
                    display_x < 0 or
                    display_x >= 79):
                self.stars.remove(star)
                self.stars.append(self.Star())
            else:
                graphic = "*"
                if(display_z < 2):
                    graphic = '·'
                elif(display_z < 4):
                    graphic = '•'
                else:
                    graphic = '*'
                if(self.graphic):
                    graphic = self.graphic
                screen.addstr(int(display_y), int(display_x), graphic)
