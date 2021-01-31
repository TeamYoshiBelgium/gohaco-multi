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

    def init(self):
        for i in range(self.L.steps_count):
            self.timescale_blocked.append({})

    def preprocess(self):
        # for book in tqdm(self.books):
        #     book.calc_library_scores()
        # print(self.orders[1], self.orders[1].orders[:20])
        with Pool(THREADS) as p:
            mount_score_tuples = p.map(self.parallelCalculation, self.mountpoints)

        self.mountpoints = map(
            lambda tup: tup[1],
            sorted(mount_score_tuples, reverse=True, key=lambda mp: mp[0])
        )

    def optimize(self):

        self.preprocess()

        self.write()
        self.analyze()

    def parallelCalculation(self, mountpoint):
        best_tasks = mountpoint.find_task_sorter(self.tasks)
        score = mountpoint.best_case_score(best_tasks)

        return (score, mountpoint)

    def write(self):
        pass

    def analyze(self):
        pass
