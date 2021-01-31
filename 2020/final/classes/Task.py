class Task:
    CNTR = 0

    def __init__(self, optimizer, score, points_count):
        self.O = optimizer
        self.score = score
        self.points_count = points_count
        self.points = []

        self.No = Task.CNTR

        self.solved = False
        self.arm = None

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "TASK%03s(%-03s/%03s)" % (self.No, self.fill, self.maxSize)
