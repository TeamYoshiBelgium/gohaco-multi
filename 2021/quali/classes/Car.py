from classes import Street

class Car:
    CNTR = 0
    drive_time = 0

    def __init__(self, O, count, streets: Street):
        self.O = O
        self.count = count
        self.streets = streets

        self.No = Car.CNTR
        Car.CNTR += 1

    def __str__(self):
        return 'CAR%i(%i %s)' % (self.id, self.score, str(self.done)[0])

    def __repr__(self):
        return str(self)

    def does_finish(self):
        return self.total_time() > self.O.duration

    def wait(self):
        self.drive_time += 1

    def drive(self, street: Street):
        self.drive_time += street.time

    def total_time(self):
        total_time = 0
        for street in self.streets:
            total_time += street.time
        return total_time

    def get_score(self):
        if self.does_finish():
            return 1000 + self.O.duration - self.drive_time
        else:
            return 0

    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No
