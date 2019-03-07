class Line:

    """Class representing Cache Line."""

    def __init__(self, mru=None):
        self.valid = 0
        self.tag = 0
        self.dirty = 0
        if mru == 0:
            self.mru = ""
        else:
            self.mru = 0