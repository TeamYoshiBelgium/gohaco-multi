class Intersection:
    def __init__(self, O, id):
        self.O = O
        self.id = id

    def __str__(self):
        return 'IS%i(%s)' % (self.id)

    def __repr__(self):
        return str(self)

    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No