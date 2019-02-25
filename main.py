

# - Game ----------------------------------------------------------------------
"""
This file is the main entry point for the game. Execute this file to play:
$ py main.py

The game is a 3D spaceship simulation. The user can fly a spaceship around a
sparsely populated solar system. The controls are as follows:

W+S: Pitch control (vertical view angle)
A+D: Yaw control (horizontal view angle)
Q+E: Roll control (rotates view screen)
Arrow Up + Down: Increase thrust, Decrease thrust

The Curses library is used throughout the project for input and output.
The game is mutithreaded, allowing for separate input and output threads
to execute concurrently. The game collects input from the player in real time,
updates the game world, and then updates a 3D game environment display. The
Game class is a singleton which handles all gameplay logic, while the Client
class is also a singleton handling input and display.
"""


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
