from tqdm import tqdm
from multiprocessing import Pool
from . import Loader

THREADS = 6

class Optimizer:
    def __init__(self, loader: Loader, swap_vs_increment_heuristic, increment_decrement_heuristic): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.L = loader
        self.swap_vs_increment_heuristic = swap_vs_increment_heuristic
        self.increment_decrement_heuristic = increment_decrement_heuristic
        self.street_usage = dict()

    def init(self):
        pass

    def preprocess(self):
        for car in tqdm(self.cars):
            for street in car.streets:
                street.end_intersection.addCar(car)

                if street.name in self.street_usage:
                    self.street_usage[street.name] += 1
                else:
                    self.street_usage[street.name] = 1
                
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
