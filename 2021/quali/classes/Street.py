class Street:
    def __init__(self, O, name, start, end, time):
        self.O = O
        self.name = name
        self.start = start
        self.end = end
        self.time = time

    def __str__(self):
        return 'STRT(%s)' % (self.name)

    def __repr__(self):
        return str(self)
    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No