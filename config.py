

# = Project Constants =========================================================

# - Screen (shell) metrics -----------------------
SCREEN_SIZE_WIDTH = 80
SCREEN_SIZE_HEIGHT = 24

# - Player command codes -------------------------
COMMAND_UP = 1
COMMAND_DOWN = 2
COMMAND_RIGHT = 4
COMMAND_LEFT = 8
COMMAND_PRIMARY = 64

# - Timing and delays ----------------------------
TIME_GAME_TICK = 1/30  # Delay between game loop iterations, in seconds

# - Messages and Strings -------------------------
MESSAGE_SCREEN_SIZE_CONDITION_NOT_MET = (
    F'Cannot start engine. Screen must be at least {SCREEN_SIZE_WIDTH} '
    F'characters wide and {SCREEN_SIZE_HEIGHT} high.')
