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
        self.arms = self.L.arms
        self.mountpoints = self.L.mount_points

        for i in range(self.L.steps_count):
            self.timescale_blocked.append({})

    def preprocess(self):
        pass
        # for book in tqdm(self.books):
        #     book.calc_library_scores()
        # print(self.orders[1], self.orders[1].orders[:20])
        # print(self.mountpoints)
        # print(list(filter(lambda mp: mp.arm is not None, self.mountpoints)))
        # with Pool(THREADS) as p:
        #     mount_score_tuples = map(self.parallelCalculation, filter(lambda mp: mp.arm is not None, self.mountpoints))
        #
        # # for mp in mount_score_tuples:
        # #     print(mp)
        #
        # self.mountpoints = map(
        #     lambda tup: tup[1],
        #       list(sorted(mount_score_tuples, reverse=True, key=lambda mp: mp[0]))
        # )
        #
        # for mp in self.mountpoints:
        #     print(mp)

    def find_best_tuple(self, list):
        best = None
        best_score = -99999999
        for el in list:
            if el[0] > best_score:
                best = el[1]
                best_score = el[0]


        return best

    def find_best_mp(self, pool):
        mount_score_tuples = map(self.parallelCalculation, list(filter(lambda mp: mp.arm is None, self.mountpoints)))
        best = self.find_best_tuple(mount_score_tuples)

        return best

    def optimize(self):
        with Pool(THREADS) as p:
            best_mountpoint = self.find_best_mp(p)

            i = 0

            while best_mountpoint is not None and i < len(self.arms):
                arm = self.arms[i]
                arm.assign(best_mountpoint)

                arm.execute_all_tasks()

                print("Assigned %s to %s" % (arm, best_mountpoint))
                i += 1

                best_mountpoint = self.find_best_mp(p)

        # for mp in mount_score_tuples:
        #     print(mp)

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
