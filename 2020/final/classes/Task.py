class Task:
    CNTR = 0

    def __init__(self, optimizer, x, y):
        self.O = optimizer
        self.x = x
        self.y = y
        self.No = Task.CNTR

        self.solved = False
        self.arm = None

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "TASK%03s(%-03s/%03s)" % (self.No, self.fill, self.maxSize)
