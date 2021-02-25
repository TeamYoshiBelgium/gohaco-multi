class Car:
    CNTR = 0

    def __init__(self, O, count, streets):
        self.O = O
        self.count = count
        self.streets = streets

        self.No = Car.CNTR
        Car.CNTR += 1

        self.currentStreetIndex = 0
        self.finished = False
        self.finishTime = -1

        self.doneStreets = [self.streets[0]]

    def driveIntersection(self):
        # car.currentIntersection = car.streets[0].end_intersection
        # car.currentIntersection.currentCars.append(car)
        # car.currentStreetIndex = 0
        # car.nextStreet = car.streets[1]

        self.doneStreets.append(self.nextStreet)
        self.currentStreetIndex += 1

        self.currentStreet = self.streets[self.currentStreetIndex]

        if self.currentStreetIndex + 1 < len(self.streets):
            self.currentIntersection = self.nextStreet.end_intersection
            self.currentIntersection.currentCars.append(self)
            self.nextStreet = self.streets[self.currentStreetIndex + 1]
        else:
            self.finished = True
            self.finishTime = self.O.currentT + self.currentStreet.time
            self.nextStreet = None

        self.blockedT = self.O.currentT + self.currentStreet.time

    def __str__(self):
        return 'CAR%i' % (self.No)

    def __repr__(self):
        return str(self)

    def total_time(self):
        total_time = 0
        for street in self.streets:
            total_time += street.time
        return total_time

    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No
