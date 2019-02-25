

# = Client Singleton ==========================================================
"""
The Client class is a singleton and must be accessed via the get_client
function. The client object represents the interface through which the player
interacts with the game. It is implemented as a hierarchy of driver objects,
each of which manages a different mode of gameplay. The central client handles
the routing of commands and delegates drawing to the sub-drivers.

The curses library is used extensively for both input and output.
"""

# - Dependencies ---------------------------------
# Python Modules
import threading
import curses
# Local Modules
from config import *
from bindings import KEY_BINDINGS
from driver import Driver
from driver_title import Title


# - Client access function -----------------------
client = None


def get_client(*arguments):
    """
    Retrieves the client singleton.
    The Client class should not be instanced directly.
    """
    global client
    # Generate a client if necessary
    if(client is None and arguments[0]):
        client = Client(arguments[0])
    # Return the client
    return client


# - Definition and initialization ----------------
class Client(Driver):
    """
    The Client class is a singleton and should be accessed via the get_client
    function. The client object manages all input and output via the curses
    library. The client is implemented as a hierarchy of "driver" objects, each
    managing input and output for a distinct aspect of gameplay.
    """

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
                # Get character code from player
                key_code = screen.getch()
                # Handle "quit" code (Ctrl+C)
                if(key_code is WINDOWS_INTERRUPT):
                    self.finished.set()
                # Translate code into Command, and execute
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
        """Routes player commands to the appropriate sub-driver."""
        self.key_command = which
        return super().command(which)

    def key_clear(self):
        """Clears all pressed keys so commands don't recur."""
        self.key_command = None

    # - Display --------------------------------------
    def display(self, screen, *args):
        """Clears the screen delegates drawing to the focused sub-driver."""
        screen.clear()
        # Do own drawing first, then draw children on top
        # Draw Children
        result = super().display(screen, *args)
        # Write buffer to screen
        screen.refresh()
        return result
