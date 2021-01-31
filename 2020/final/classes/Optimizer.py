from tqdm import tqdm
from multiprocessing import Pool
from . import Loader

THREADS = 6

class Optimizer:
    def __init__(self, loader: Loader): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.L = loader

        self.timescale_blocked = []

    def init(self):
        self.tasks = self.L.tasks
        self.arms = []
        self.mountpoints = self.L.mount_points

        for i in range(self.L.steps_count):
            self.timescale_blocked.append({})

    def preprocess(self):
        # for book in tqdm(self.books):
        #     book.calc_library_scores()
        # print(self.orders[1], self.orders[1].orders[:20])
        with Pool(THREADS) as p:
            mount_score_tuples = map(self.parallelCalculation, self.mountpoints)

        # for mp in mount_score_tuples:
        #     print(mp)

        self.mountpoints = map(
            lambda tup: tup[1],
              list(sorted(mount_score_tuples, reverse=True, key=lambda mp: mp[0]))
        )

        for mp in self.mountpoints:
            print(mp)


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
