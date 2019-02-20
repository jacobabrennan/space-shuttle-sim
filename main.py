

# - Game ----------------------------------------------------------------------

# - Dependencies ---------------------------------
# Python Modules
import curses
import threading
import time
# Local Modules
from config import *
from client import get_client
from game import get_game


# - Create and start Game ------------------------
def main(standard_screen):
    # Determine if shell is configured properly to play
    size = standard_screen.getmaxyx()
    if(size[1] < SCREEN_CHARACTER_WIDTH or size[0] < SCREEN_CHARACTER_HEIGHT):
        print(MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET)
        exit(1)
    # Configure Curses (shell display)
    curses.curs_set(False)  # Make the cursor invisible
    curses.cbreak()  # Make keyboard input non-breaking
    standard_screen.keypad(True)  # Enable use of arrow keys
    # Create Client and Game
    client = get_client(standard_screen)
    game = get_game(standard_screen)
    client.finished.wait()
    exit(0)

# - Start Main ---------------------------------------
curses.wrapper(main)
