

# = Project Constants =========================================================

# - Dependencies ---------------------------------
# Python Modules
# Local Modules

# - Notes ----------------------------------------
# Characters are 8x12 pixels.
# A terminal window of 80x24 characters is thus 640x288px.
# This is an aspect ratio of 20:9.
# The Spaceship's cockpit window will be 2 x 0.9 meters.


# - Screen (shell) metrics -----------------------
SCREEN_SIZE_WIDTH = 80
SCREEN_SIZE_HEIGHT = 24
WINDOWS_INTERRUPT = 3

# - Player command codes -------------------------
COMMAND_UP = 1
COMMAND_DOWN = 2
COMMAND_RIGHT = 4
COMMAND_LEFT = 8
COMMAND_PRIMARY = 64

# - Timing and delays ----------------------------
TIME_GAME_TICK = 1/30  # Delay between game loop iterations, in seconds

# - Math -----------------------------------------
# Measures
AU = 149597870700
KILO = 1000
MEGA = 1000*KILO
GIGA = 1000*MEGA


# - Messages and Strings -------------------------
MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET = (
    F'Cannot start engine. Screen must be at least {SCREEN_SIZE_WIDTH} '
    F'characters wide and {SCREEN_SIZE_HEIGHT} high.')
