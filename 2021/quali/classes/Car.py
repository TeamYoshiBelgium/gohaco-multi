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

        self.currentStreetIndex = 0
        self.finished = False
        self.finishTime = -1
        self.blockedT = 0
        self.doneStreets = [self.streets[0]]

    def driveIntersection(self):
        # car.currentIntersection = car.streets[0].end_intersection
        # car.currentIntersection.currentCars.append(car)
        # car.currentStreetIndex = 0
        # car.nextStreet = car.streets[1]

        self.doneStreets.append(self.nextStreet)

        # print(str(self) + ", OT" + str(self.O.currentT) + ", B" + str(self.blockedT) + "," + str(self.nextStreet.time))

        self.blockedT = self.O.currentT + self.nextStreet.time


        self.currentStreetIndex += 1

        self.currentStreet = self.streets[self.currentStreetIndex]

        if self.currentStreetIndex + 1 < len(self.streets):
            self.currentIntersection = self.nextStreet.end_intersection
            self.currentIntersection.addNewCar(self, self.blockedT, self.nextStreet)
            self.nextStreet = self.streets[self.currentStreetIndex + 1]
        else:
            self.finished = True
            self.finishTime = self.blockedT #self.O.currentT + self.nextStreet.time
            self.nextStreet = None


    def __str__(self):
        return 'CAR%i' % (self.No)

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
        if self.finished and self.finishTime <= self.O.duration:
            return self.O.score + self.O.duration - self.finishTime
        else:
            return 0

    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No
