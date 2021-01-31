class MountPoint:
    CNTR = 0

    def __init__(self, optimizer, id, point):
        self.O = optimizer
        self.id = id
        self.point = point

        self.No = MountPoint.CNTR

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "MPNT%03s(%-03s/%03s)" % (self.No, self.point.x, self.point.y)