from math import copysign

import numpy as np

from .Instruction import Instruction
from .Optimizer import Optimizer

class Arm:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, id, x, y):
        self.O = optimizer
        self.x = x
        self.y = y
        self.id = id
        self.No = id

        self.tasks: [Task] = []
        self.instructions: [Instruction] = []

        self.mountpoint = None

        self.time = 0
        self.score = 0

    def assign(self, mountpoint):
        self.mountpoint = mountpoint
        self.x = mountpoint.x
        self.y = mountpoint.y

        self.O.L.map[self.y][self.x] = 1
        mountpoint.arm = self

    def exec_task(self, task):
        self.score += task.score
        self.tasks.append(task)

        all_moves = task.get_moves(self)

        self.time += len(all_moves)

        if len(all_moves) > 0:
            prev_x = self.x
            prev_y = self.y

            self.O.L.map[self.y][self.x] = 0

            for point_tup in all_moves:
                self.instructions.append(Instruction(self.O, self, prev_x, prev_y, point_tup[0], point_tup[1]))

                x = point_tup[0]
                y = point_tup[1]

                self.O.L.map[y][x] = 0

                prev_x = x
                prev_y = y

                self.x = prev_x
                self.y = prev_y

        task.solved = True

    def execute_all_tasks(self):
        next_task = self.find_best_next_task()

        while next_task is not None:
            self.exec_task(next_task)

            next_task = self.find_best_next_task()

    def find_best_next_task(self):
        best = None
        best_score = -99999
        
        for task in self.O.tasks:
            if task.solved is True:
                continue

            result = task.get_score_and_moves(self)
            if result is None:
                continue

            (score, moves) = result

            if self.time + moves > self.O.L.steps_count:
                continue

            ratio = score / max(1, moves)

            if ratio > best_score:
                best = task
                best_score = ratio

        return best
    #
    # def go_to_point(self, point: Point):
    #     while self.x != point.x:
    #         instruction = Instruction(self.O, self, self.x, self.y, self.x + np.sign(self.x - point.x), self.y)
    #         self.exec_instruction(instruction)
    #     while self.y != point.y:
    #         instruction = Instruction(self.O, self, self.x, self.y, self.x, self.y + np.sign(self.y - point.y))
    #         self.exec_instruction(instruction)
    #
    # def exec_instruction(self, instruction: Instruction):
    #     self.instructions.append(instruction)
    #     self.x = instruction.x2
    #     self.y = instruction.y2
    #     self.blocked.append({'x': instruction.x2, 'y': instruction.y2})

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ARM%03s(%-03s/%03s)" % (self.No, self.x, self.y)
