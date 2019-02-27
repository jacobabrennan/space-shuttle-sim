

# = Project Constants =========================================================
"""
Defined herein are the various constants used throughout the game, centralized
for consistency and ease of modification.
"""


# - Dependencies ---------------------------------
# Python Modules
import math
# Local Modules

# - Notes ----------------------------------------
# Characters are 8x12 pixels.
# A terminal window of 80x24 characters is thus 640x288px.
# This is an aspect ratio of 20:9.
# The Spaceship's cockpit window will be 2 x 0.9 meters.


# - Screen (shell) metrics -----------------------
WINDOWS_INTERRUPT = 3
CHARACTER_WIDTH = 8
CHARACTER_HEIGHT = 12
SCREEN_CHARACTER_WIDTH = 80
SCREEN_CHARACTER_HEIGHT = 24
SCREEN_PIXEL_WIDTH = SCREEN_CHARACTER_WIDTH * CHARACTER_WIDTH
SCREEN_PIXEL_HEIGHT = SCREEN_CHARACTER_HEIGHT * CHARACTER_HEIGHT
SCREEN_PHYSICAL_WIDTH = 2
SCREEN_PHYSICAL_HEIGHT = 0.9

# - Player command codes -------------------------
COMMAND_UP = 1
COMMAND_DOWN = 2
COMMAND_RIGHT = 4
COMMAND_LEFT = 8
COMMAND_ROLL_ANTICLOCK = 16
COMMAND_ROLL_CLOCKWISE = 32
COMMAND_FORWARD = 64
COMMAND_BACK = 128
COMMAND_PRIMARY = 256
COMMAND_STABILIZE = 512
COMMAND_TIME_SCALE_INCREASE = 1024
COMMAND_TIME_SCALE_DECREASE = 2048


# - Timing and delays ----------------------------
TIME_GAME_TICK = 1/30  # Delay between game loop iterations, in seconds

# - Math -----------------------------------------
# Really really important stuff
GRAVITATIONAL_CONSTANT = 6.674e-11
# Measures
KILO = 1000
MEGA = 1000*KILO
GIGA = 1000*MEGA
TERA = 1000*GIGA
# Distances
AU = 149597870700
LY = 9.46*TERA*KILO
PARSEC = 30856775814913700
# Time
SECOND = TIME_GAME_TICK/TIME_GAME_TICK
MINUTE = 60 * SECOND
HOUR = 60 * MINUTE
DAY = 24 * HOUR
YEAR = 365 * DAY

# - Player Vehicle Metrics -----------------------
SHIP_TURNING_ANGLE = math.pi / 360
SHUTTLE_THRUST_MAX = 2279*KILO
SHUTTLE_MASS = 74842

# - Messages and Strings -------------------------
MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET = (
    F'Cannot start engine. Screen must be at least {SCREEN_CHARACTER_WIDTH} '
    F'characters wide and {SCREEN_CHARACTER_HEIGHT} high.')
