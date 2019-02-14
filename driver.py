

# = Driver ====================================================================

class Driver:
    """
    Driver is a class which represents any structure for handling client input
    and output. display and command are the main methods provided for override
    by subclasses. Both methods, by default, invoke the same method on their
    current_focus. Both should return True to indicate they are "blocking".
    For example, a sub-driver might wish to indicate that it has handled player
    keyboard input, and no further handling should be performed by the parent.
    """

    def __init__(self):
        self.current_focus = False

    def focus(self, newFocus):
        """
        Called to focus the client on this input for input / output.
        Display and commands are automatically routed to their current focus.
        """
        # Blur any old focus
        if(self.current_focus):
            self.blur()
        # Set new focus, and alert newFocus of focus
        self.current_focus = newFocus
        if(self.current_focus):
            self.current_focus.focused()

    def blur(self):
        """Called to remove focus from self and any child drivers."""
        # Blur any child drivers
        if(self.current_focus):
            self.current_focus.blurred()
        # Unset focus
        self.current_focus = False

    def focused(self):
        """A hook for subclasses to add behavior when they recieve focus."""
        # Hook
        return

    def blurred(self):
        """A hook for subclasses to add behavior after they lose focus."""
        # Hook
        return

    def command(self, which):
        """
        A hook for subclasses to extend in order to handle player input.
        Subclasses must call the super in order to pass commands to children,
        and should check the return value to determine if the child has
        blocked further commands.
        Subclasses should return a True value if they wish to block parents.
        """
        # By default, do nothing except pass commands to focused child
        if(not self.current_focus):
            return False
        return self.current_focus.command(which)

    def display(self, screen, **options):
        """
        A hook for subclasses to extend to display output to the player.
        Subclasses must call the super in order to allow children to draw.
        Super should generally be called after any custom drawing, so that
        children will be drawn on top of the parent.
        Subclasses may return True to indicate blocking.
        """
        # By default, do nothing except draw focused child
        if(not self.current_focus):
            return False
        return self.current_focus.display(screen, **options)
