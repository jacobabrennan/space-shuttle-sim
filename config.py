

# = Project Constants =========================================================

# - Dependencies ---------------------------------
# Language Modules
import math

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


# - Positions and Vectors ------------------------
def vector_between(S, E):
    """Calculates the vector between S and E (start and end)."""
    return (E[0]-S[0], E[1]-S[1], E[2]-S[2])


def distance(S, E):
    """Calculates the distance between S and E (start and end)."""
    return math.sqrt((E[0]-S[0])**2 + (E[1]-S[1])**2 + (E[2]-S[2])**2)


def magnitude(V):
    """Calculates the magnitude of a given vector."""
    return math.sqrt(V[0]**2 + V[1]**2 + V[2]**2)


# - Messages and Strings -------------------------
MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET = (
    F'Cannot start engine. Screen must be at least {SCREEN_SIZE_WIDTH} '
    F'characters wide and {SCREEN_SIZE_HEIGHT} high.')
