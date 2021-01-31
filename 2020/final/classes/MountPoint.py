from . import Optimizer

class MountPoint:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, id, x, y):
        self.O = optimizer
        self.id = id
        self.x = x
        self.y = y

        self.No = id

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "MPNT%03s(%-03s/%03s)" % (self.No, self.x, self.y)