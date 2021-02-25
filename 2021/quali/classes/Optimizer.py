from tqdm import tqdm
from multiprocessing import Pool
from . import Loader

THREADS = 6

class Optimizer:
    def __init__(self, loader: Loader, swap_vs_increment_heuristic, increment_decrement_heuristic): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.L = loader
        self.swap_vs_increment_heuristic = swap_vs_increment_heuristic
        self.increment_decrement_heuristic = increment_decrement_heuristic
        self.first_street_usage = []
        self.street_usage = []

        # self.O.cars
        # self.O.duration
        # self.O.intersections
        # self.O.intersections_dict
        # self.O.score
        # self.O.streets
        # self.O.streets_dict

        self.currentT = 0

    def init(self):
        pass

    def preprocess(self):

        street_first_usage_dict = dict()
        street_usage_dict = dict()
        for car in tqdm(self.cars):

            first_street = car.streets[0]
            if first_street.name in street_first_usage_dict:
                street_first_usage_dict[first_street.name] += 1
            else:
                street_first_usage_dict[first_street.name] = 1

            for street in car.streets:
                street.end_intersection.addCar(car)

                if street.name in street_usage_dict:
                    street_usage_dict[street.name] += 1
                else:
                    street_usage_dict[street.name] = 1

        for key in street_usage_dict.keys():
            self.street_usage.append((key, street_usage_dict[key]))

        for key in street_first_usage_dict.keys():
            self.first_street_usage.append((key, street_first_usage_dict[key]))

        self.first_street_usage.sort(key=lambda tup: tup[1], reverse=True)


        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):
        self.preprocess()

        self.duration = 10
        self.updateGlobalState()

        for car in self.cars:
            print("%s %s %s\n\r  %s\n\r  %s" % (car, car.finished, car.finishTime, car.doneStreets, car.streets))

        # with Pool(THREADS) as p:
        #     while True:
        #         p.map(self.parallelCalculation, [])

        self.write()
        self.analyze()

    def updateGlobalState(self):
        self.currentT = 0

        for intersection in self.intersections:
            intersection.currentCars = []
            intersection.currentTimeSlot = 0
            intersection.maxTime = sum(map(lambda tup: tup[0], intersection.trafficLightStreetTuples))

        for car in self.cars:
            car.blockedTill = 0
            car.currentIntersection = car.streets[0].end_intersection
            car.currentIntersection.currentCars.append(car)
            car.currentStreetIndex = 0
            car.currentStreet = car.streets[0]
            car.nextStreet = car.streets[1]
            car.finished = False
            car.doneStreets = [car.currentStreet]

        for i in range(self.duration):
            self.currentT = i
            print(i)

            for intersection in self.intersections:
                intersection.currentTimeSlot += 1
                if intersection.currentTimeSlot >= intersection.maxTime:
                    intersection.currentTimeSlot = 0

                car = intersection.driveNextCar()
                # print(car)


    def parallelCalculation(self, objects):
        pass

    def write(self):
        pass

    def analyze(self):
        pass
