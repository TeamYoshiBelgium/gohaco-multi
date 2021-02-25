class Car:
    CNTR = 0

    def __init__(self, O, count, streets):
        self.O = O
        self.count = count
        self.streets = streets

        self.No = Car.CNTR
        Car.CNTR += 1

    def __str__(self):
        return 'CAR%i(%i %s)' % (self.id, self.score, str(self.done)[0])

    def __repr__(self):
        return str(self)

    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No
