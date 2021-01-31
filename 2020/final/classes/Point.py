class Point:
    def __init__(self, optimizer, id, x, y):
        self.O = optimizer
        self.id = id
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "Point%03s(%-03s/%03s)" % (self.id, self.x, self.y)
