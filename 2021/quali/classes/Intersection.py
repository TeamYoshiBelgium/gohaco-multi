
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

        tuple = self.intersection.trafficLightStreetTuples[first]
        self.intersection.trafficLightStreetTuples[first] = self.intersection.trafficLightStreetTuples[second]
        self.intersection.trafficLightStreetTuples[second] = tuple

class ChangeWeightMutation(Mutation):
    def __init__(self, intersection):
        super(ChangeWeightMutation, self).__init__(MutationType.CHANGE_WEIGHT, intersection)

    def getTrafficLightStreetTuples(self):
        first = random.randint(0, len(self.intersection.trafficLightStreetTuples))

        self.intersection.trafficLightStreetTuples[first][0] = random.randint(1, self.intersection.O.duration)

class Intersection:
    def __init__(self, O, id, streets):
        self.O = O
        self.id = id
        self.streets = streets

        self.trafficLightStreetTuples = []
        self.carsThatPassThrough = []

        for street in self.streets:
            self.trafficLightStreetTuples.append((1, street))

    def mutationScore(self):
        pass

    def generateMutation(self):
        if random.random() > self.O.swap_vs_increment_heuristic:
            mutation = SwapMutation(self)
        else:
            mutation = ChangeWeightMutation(self)

        return mutation

    def addCar(self, car):
        self.carsThatPassThrough.append(car)

    def __str__(self):
        return 'IS%i(%s)' % (self.id)

    def __repr__(self):
        return str(self)
    #
    # def __gt__(self, other):
    #     return self.No > other.No
    #
    # def __lt__(self, other):
    #     return self.No > other.No