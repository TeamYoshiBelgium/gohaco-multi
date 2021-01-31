from . import Optimizer

class Arm:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, x, y):
        self.O = optimizer
        self.x = x
        self.y = y
        self.No = Arm.CNTR

        self.tasks = []
        self.instructions = []

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ARM%03s(%-03s/%03s)" % (self.No, self.x, self.y)
