
import random
from enum import Enum
from abc import ABC, abstractmethod

class MutationType(Enum):
    SWAP = 1
    CHANGE_WEIGHT = 2

class Mutation(ABC):
    def __init__(self, type, intersection):
        self.cached = None
        self.type = type
        self.intersection = intersection

    @abstractmethod
    def getTrafficLightStreetTuples(self):
        pass

class SwapMutation(Mutation):
    def __init__(self, intersection):
        self.cached = None
        super(SwapMutation, self).__init__(MutationType.SWAP, intersection)

    def getTrafficLightStreetTuples(self):
        if self.cached is not None:
            return self.cached

        first = random.randint(0, len(self.intersection.trafficLightStreetTuples) - 1)
        second = random.randint(0, len(self.intersection.trafficLightStreetTuples) - 1)

        if first == second:
            second = (first + 1) % len(self.intersection.trafficLightStreetTuples)

        newList = self.intersection.trafficLightStreetTuples.copy()

        tuple = self.intersection.trafficLightStreetTuples[first]
        newList[first] = self.intersection.trafficLightStreetTuples[second]
        newList[second] = tuple

        self.cached = newList

        return newList

class ChangeWeightMutation(Mutation):
    def __init__(self, intersection):
        super(ChangeWeightMutation, self).__init__(MutationType.CHANGE_WEIGHT, intersection)

    def getTrafficLightStreetTuples(self):
        if self.cached is not None:
            return self.cached

        newList = self.intersection.trafficLightStreetTuples.copy()
        randIx = random.randint(0, len(newList) - 1)
        randEl = newList[randIx]

        if randEl[0] == 0:
            newList[randIx] = (1, randEl[1])
        else:
            if random.random() < self.intersection.O.increment_decrement_heuristic:
                newList[randIx] = (randEl[0] + 1, randEl[1])
            else:
                newList[randIx] = (randEl[0] - 1, randEl[1])

        self.cached = newList
        return newList


class Intersection:
    def __init__(self, O, id, streets):
        self.O = O
        self.id = id
        self.streets = streets

        self.trafficLightStreetTuples = []
        self.carsThatPassThrough = []

        # for street in self.streets:
        #     self.trafficLightStreetTuples.append((1, street))

        street_usage = []
        for street in self.streets:
            if street.name in self.O.first_street_usage:
                street_usage.append((street, self.O.first_street_usage[street.name]))
            else:
                street_usage.append((street, 0))

        street_usage.sort(key=lambda tup: tup[1], reverse=True)

        for tuple in street_usage:
            self.trafficLightStreetTuples.append((1, tuple[0]))

        self.currentCars = []
        self.currentTimeSlot = 0
        self.maxTime = 0
        self.carArrivals = {}
        for street in streets:
            self.carArrivals[street] = []

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

        return trafficLights[len(trafficLights) - 1][1]


    def addNewCar(self, car, driveTime, fromStreet):
        self.carArrivals[fromStreet].append((driveTime, car))
        self.currentCars.append(car)

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

    def generateMutationAndReturnScore(self):
        mutation = self.generateMutation()
        score = self.mutationScore(mutation)

        return (score, mutation)

    def mutationScore(self, mutation):
        newTrafficLights = mutation.getTrafficLightStreetTuples()

        oldWait = self.calcWaitingTime(self.trafficLightStreetTuples)
        newWait = self.calcWaitingTime(newTrafficLights)

        return oldWait - newWait

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
            timeslot += 1
            if timeslot >= maxTime:
                timeslot = 0

            street = self.getCurrentGreenStreetSL(timeslot, trafficLights)
            cars = sortedArrivals[street]

            if len(cars) > 0:
                if cars[0][0] <= T:
                    totalWaitingTime += T - cars[0][0]

                    if len(cars) > 1:
                        sortedArrivals[street] = sortedArrivals[street][1:]
                    else:
                        sortedArrivals[street] = []

        return totalWaitingTime

    def generateMutation(self):
        if random.random() < self.O.swap_vs_increment_heuristic:
            mutation = SwapMutation(self)
        else:
            mutation = ChangeWeightMutation(self)

        return mutation

    def addStartCar(self, car):
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