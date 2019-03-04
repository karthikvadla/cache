class Line:

    """Class representing Cache Line."""

    def __init__(self, size):
        self.valid = 0
        self.tag = 0
        self.dirty = 0
        self.data = [0] * size
