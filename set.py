from line import Line

class Set(object):
    """Cache sets"""
    def __init__(self, num_ways, replacement_policy):
        if num_ways == 1:
            self.lines = [Line() for i in range(num_ways)]
        else:
            self.lines = [Line(mru=replacement_policy) for i in range(num_ways)]
