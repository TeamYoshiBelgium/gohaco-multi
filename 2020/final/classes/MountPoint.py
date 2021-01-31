from . import Optimizer

class MountPoint:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, id, x, y):
        self.O = optimizer
        self.id = id
        self.x = x
        self.y = y

        self.No = id

    def score(self):


    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "MPNT%03s(%-03s/%03s)" % (self.No, self.x, self.y)

    def find_task_sorter(self, tasks):
        results = []

        for task in tasks:
            score = task.get_score_per_moves(self)
            result = (score, task)
            results.append(result)

        results.sort(key=lambda x: x[0], reverse=True)
