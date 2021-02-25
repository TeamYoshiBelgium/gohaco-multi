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

        with Pool(THREADS) as p:
            while True:
                p.map(self.parallelCalculation, [])

        self.write()
        self.analyze()

    def parallelCalculation(self, objects):
        pass

    def write(self):
        pass

    def analyze(self):
        pass
