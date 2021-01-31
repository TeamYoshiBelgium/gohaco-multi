from tqdm import tqdm
from multiprocessing import Pool
from . import Loader

THREADS = 6

class Optimizer:
    def __init__(self, loader: Loader): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.L = loader

        self.tasks = []
        self.arms = []
        self.mountpoints = []

        self.timescale_blocked = []
        for i in range(loader.steps_count):
            self.timescale_blocked.append({})


    def init(self):
        pass

    def preprocess(self):
        # for book in tqdm(self.books):
        #     book.calc_library_scores()
        # print(self.orders[1], self.orders[1].orders[:20])
        pass

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
