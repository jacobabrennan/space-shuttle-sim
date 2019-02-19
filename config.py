

# = Project Constants =========================================================

# - Dependencies ---------------------------------
# Python Modules
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


# - Messages and Strings -------------------------
MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET = (
    F'Cannot start engine. Screen must be at least {SCREEN_SIZE_WIDTH} '
    F'characters wide and {SCREEN_SIZE_HEIGHT} high.')


# - Positions and Vectors ------------------------
def unit_vector(V):
    """Calculates a vector of magnitude 1 in the direction of vector V."""
    return scale_vector_3d(V, 1/magnitude_3d(V))


def vector_between_3d(S, E):
    """Calculates the vector between S and E (start and end)."""
    return (E[0]-S[0], E[1]-S[1], E[2]-S[2])


def distance_3d(S, E):
    """Calculates the distance between S and E (start and end)."""
    return math.sqrt((E[0]-S[0])**2 + (E[1]-S[1])**2 + (E[2]-S[2])**2)


def magnitude_3d(V):
    """Calculates the magnitude of a given vector."""
    return math.sqrt(V[0]**2 + V[1]**2 + V[2]**2)


def scale_vector_3d(V, scale):
    """Scales vector V by the scalar scale."""
    return (V[0]*scale, V[1]*scale, V[2]*scale)


def scalar_product_3d(A, B):
    """Calculates the scalar product (dot product) of vectors A and B."""
    return A[0]*B[0] + A[1]*B[1] + A[2]*B[2]


def scalar_projection_3d(A, B):
    """Calculates the scalar projection of A onto B."""
    return scalar_product_3d(A, U) / magnitude_3d(B)


def vector_projection_3d(A, B):
    """Calculates the vector projection of A onto B."""
    return scale_vector_3d(
        unit_vector(A),
        scalar_projection_3d(A, B),
    )
