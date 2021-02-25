from tqdm import tqdm
from multiprocessing import Pool
from . import Loader

THREADS = 6

class Optimizer:
    def __init__(self, loader: Loader, swap_vs_increment_heuristic, increment_decrement_heuristic): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.L = loader
        self.swap_vs_increment_heuristic = swap_vs_increment_heuristic
        self.increment_decrement_heuristic = increment_decrement_heuristic

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
        for car in tqdm(self.cars):
            for street in car.streets:
                street.end_intersection.addCar(car)
                
        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):

        self.preprocess()

        self.updateGlobalState()
        for car in self.cars:
            print("%s %s %s" % (car, car.finished, car.finishTime))

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

        for i in range(self.duration):
            self.currentT = i
            for intersection in self.intersections:
                intersection.currentTimeSlot += 1
                if intersection.currentTimeSlot >= intersection.maxTime:
                    intersection.currentTimeSlot = 0

                car = intersection.driveNextCar()




    def parallelCalculation(self, objects):
        pass

    def write(self):
        pass

    def analyze(self):
        pass
