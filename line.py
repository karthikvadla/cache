class Line:

    """Class representing Cache Line."""

    def __init__(self, lru=None):
        self.valid = 0
        self.tag = 0
        self.dirty = 0
        self.lru = lru