

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
import game


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
        the_game = game.get_game()
        the_game.start()

    # - Display --------------------------------------
    def display(self, screen, *args):
        # Check for blocking children
        block = super().display(screen, *args)
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
            line_pos,
            int((window_width-len(press_space))/2),
            ''.join([" " for char in press_space]))
        screen.addstr(
            line_pos+1,
            int((window_width-len(press_space))/2),
            press_space)
        #
        return True

    class Star:
        def __init__(self):
            self.x = random.random() - 1/2
            self.y = random.random() - 1/2
            self.z = 1

    def star_field(self):
        self.stars = []
        for index in range(1, 100):
            new_star = self.Star()
            new_star.z = random.random()*1
            self.stars.append(new_star)

    def star_advance(self, screen):
        old_stars = list(self.stars)
        for star in old_stars:
            display_x = star.x / star.z
            display_x = (display_x + 1/2) * SCREEN_CHARACTER_WIDTH
            display_x = int(display_x)
            display_y = star.y / star.z
            display_y = (display_y + 1/2) * SCREEN_CHARACTER_HEIGHT
            display_y = int(display_y)
            star.z -= 0.03
            if(
                    star.z <= 0 or
                    display_y >= 24 or
                    display_y < 0 or
                    display_x < 0 or
                    display_x >= 79):
                self.stars.remove(star)
                self.stars.append(self.Star())
            else:
                graphic = "*"
                delta = max(abs(star.x), abs(star.y))
                style = curses.A_NORMAL
                if(delta > 1/8 or star.z > 1.5):
                    graphic = '·'
                elif(star.z > 1/3):
                    graphic = '•'
                else:
                    graphic = "@"
                if(self.graphic):
                    graphic = self.graphic
                screen.addstr(int(display_y), int(display_x), graphic, style)
