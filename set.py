from line import Line

class Set(object):
    """Cache sets"""
    def __init__(self, num_ways, line_size):
        self.lines = [Line(line_size) for i in range(num_ways)]
