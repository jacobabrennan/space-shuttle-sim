

# = Gameplay Screen ===========================================================

# - Dependencies ---------------------------------
# Python Modules
import random
# Local Modules
from config import *
from driver import Driver
import client


# = Gameplay Screen Definition ================================================

# - Initialization -------------------------------
class Gameplay(Driver):
    # def __init__(self):
    #    pass

    # - Interaction ----------------------------------

    # - Display Functions ----------------------------
    def display(self, screen, **options):
        #
        the_client = client.get_client()
        command = the_client.last_command
        #
        screen.addstr(0, 0, "Gameplay Screen")
        screen.addstr(11, 28, F'Random Integer: {random.randint(1000,9999)}')
        screen.addstr(13, 28, F'Last Client Command: {command}')
