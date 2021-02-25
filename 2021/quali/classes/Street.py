class Street:
    def __init__(self, O, name):
        self.O = O
        self.name = name

    def __str__(self):
        return 'STRT%i(%s)' % (self.name)

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No