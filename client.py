

# = Client Singleton ==========================================================

# - Dependencies ---------------------------------
# Python Modules
import threading
import curses
# Local Modules
from config import *
from driver import Driver
from driver_title import Title

# - Project Constants ----------------------------
KEY_BINDINGS = {
    curses.KEY_UP: COMMAND_UP,
    curses.KEY_DOWN: COMMAND_DOWN,
    curses.KEY_RIGHT: COMMAND_RIGHT,
    curses.KEY_LEFT: COMMAND_LEFT,
    ord(' '): COMMAND_PRIMARY,
}

# - Client access function -----------------------
client = None


def get_client(*arguments):
    global client
    # Generate a client if necessary
    if(client is None and arguments[0]):
        client = Client(arguments[0])
    # Return the client
    return client


# - Definition and initialization ----------------
class Client(Driver):
    def __init__(self, screen):
        super().__init__()
        self.key_command = None
        self.last_command = None
        # Show Title
        self.focus(Title())
        # Setup Input Thread
        self.finished = threading.Event()

        def input_loop(screen):
            while(True):
                key_code = screen.getch()
                if(key_code is WINDOWS_INTERRUPT):
                    self.finished.set()
                else:
                    print(F'Code: {key_code}')
                self.last_command = chr(key_code)
                if(key_code in KEY_BINDINGS):
                    self.command(KEY_BINDINGS[key_code])
        thread_input = threading.Thread(
            target=input_loop,
            name="Input Loop",
            daemon=True,
            args=(screen,))
        thread_input.start()

    # - Keyboard handling ----------------------------
    def command(self, which):
        self.key_command = which
        return super().command(which)

    def key_clear(self):
        self.key_command = None

    # - Display --------------------------------------
    def display(self, screen, **options):
        screen.clear()
        # Do own drawing first, then draw children on top
        # Draw Children
        result = super().display(screen, **options)
        # Write buffer to screen
        screen.refresh()
        return result
