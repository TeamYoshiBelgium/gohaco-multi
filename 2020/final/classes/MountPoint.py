from . import Optimizer

class MountPoint:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, id, x, y):
        self.O = optimizer
        self.id = id
        self.x = x
        self.y = y

        self.No = id

        self.arm = None

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "MPNT%03s(%-03s/%03s,%s)" % (self.No, self.x, self.y, self.arm)


    def find_task_sorter(self, tasks):
        results = []

        for task in tasks:
            score = task.get_score_per_moves(self)
            if score > 0:
                result = (score, task)
                results.append(result)

        results.sort(key=lambda x: x[0], reverse=True)

        return results

    def best_case_score(self, task_tuples):
        steps = 0
        score = 0
        i = 0
        while steps < self.O.L.steps_count and i < len(task_tuples):
            if i > len(task_tuples):
                return score

            score += task_tuples[i][1].score
            steps += task_tuples[i][1].get_score_and_moves(self)[1]

            i += 1

        return score