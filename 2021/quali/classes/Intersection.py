
import random
from enum import Enum
from abc import ABC, abstractmethod

class MutationType(Enum):
    SWAP = 1
    CHANGE_WEIGHT = 2

class Mutation(ABC):
    def __init__(self, type, intersection):
        self.type = type
        self.intersection = intersection

    @abstractmethod
    def getTrafficLightStreetTuples(self):
        pass

class SwapMutation(Mutation):
    def __init__(self, intersection):
        super(SwapMutation, self).__init__(MutationType.SWAP, intersection)

    def getTrafficLightStreetTuples(self):
        first = random.randint(0, len(self.intersection.trafficLightStreetTuples))
        second = random.randint(0, len(self.intersection.trafficLightStreetTuples))

        if first == second:
            second = (first + 1) % len(self.intersection.trafficLightStreetTuples)

        newList = self.intersection.trafficLightStreetTuples.copy()

        tuple = self.intersection.trafficLightStreetTuples[first]
        newList[first] = self.intersection.trafficLightStreetTuples[second]
        newList[second] = tuple

        return newList

class ChangeWeightMutation(Mutation):
    def __init__(self, intersection):
        super(ChangeWeightMutation, self).__init__(MutationType.CHANGE_WEIGHT, intersection)

    def getTrafficLightStreetTuples(self):
        newList = self.intersection.trafficLightStreetTuples.copy()
        randIx = random.randInt(0, len(newList))
        randEl = newList[randIx]

        if randEl[0] == 0:
            newList[randIx] = (1, randEl[1])
        else:
            if random.random() < self.intersection.O.increment_decrement_heuristic:
                newList[randIx] = (randEl[0] + 1, randEl[1])
            else:
                newList[randIx] = (randEl[0] - 1, randEl[1])

        return newList


class Intersection:
    def __init__(self, O, id, streets):
        self.O = O
        self.id = id
        self.streets = streets

        self.trafficLightStreetTuples = []
        self.carsThatPassThrough = []

        for street in self.streets:
            self.trafficLightStreetTuples.append((1, street))

        self.currentCars = []
        self.currentTimeSlot = 0
        self.maxTime = 0

    # def calcScore(self, trafficLightStreetTuples):

    def getCurrentGreenStreet(self):
        timeSlot = self.currentTimeSlot
        for tup in self.trafficLightStreetTuples:
            if timeSlot - tup[0] < 0:
                return tup[1]
            else:
                timeSlot -= tup[0]

    def getCurrentGreenStreetSL(self, currentTimeslot, trafficLights):
        timeSlot = currentTimeslot
        for tup in trafficLights:
            if timeSlot - tup[0] < 0:
                return tup[1]
            else:
                timeSlot -= tup[0]

    def driveNextCar(self):
        greenStreet = self.getCurrentGreenStreet()

        for car in self.currentCars:
            if car.blockedT > self.O.currentT:
                continue

            if car.finished is True:
                continue

            if car.currentStreet == greenStreet:
                car.driveIntersection()
                self.currentCars.remove(car)
                return car

    def mutationScore(self):
        mutation = self.generateMutation()
        newTrafficLights = mutation.getTrafficLightStreetTuples()

    def calcWaitingTime(self, trafficLights):
        sortedArrivals = {}
        doneArrivals = {}
        for key in self.carArrivals:
            sortedArrivals[key] = list(sorted(self.carArrivals[key], key=lambda tup: tup[0]))
        # carArrivals = list(sorted(self.carArrivals, key=lambda tup: tup[1]))

        maxTime = sum(map(lambda tup: tup[0], trafficLights))
        timeslot = 0

        totalWaitingTime = 0

        for T in range(self.O.duration):
            street = self.getCurrentGreenStreetSL(timeslot, trafficLights)
            cars = sortedArrivals[street]

            if len(cars) > 0:
                if cars[0][0] <= T:
                    totalWaitingTime += T - cars[0][0]

                    if len(cars) > 1:
                        sortedArrivals[street] = sortedArrivals[street][1:]

            timeslot += 1
            if timeslot >= maxTime:
                timeslot = 0

    def generateMutation(self):
        if random.random() > self.O.swap_vs_increment_heuristic:
            mutation = SwapMutation(self)
        else:
            mutation = ChangeWeightMutation(self)

        return mutation

    def addCar(self, car):
        self.carsThatPassThrough.append(car)

    def __str__(self):
        return 'IS(%i)' % (self.id)

    def __repr__(self):
        return str(self)
    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No