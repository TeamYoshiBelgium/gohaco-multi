from math import copysign

import numpy as np

from .Instruction import Instruction
from .Optimizer import Optimizer
from .Point import Point

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
        self.blocked: [{x: int, y: int}] = []
        for i in range(self.O.L.steps_count):
            self.blocked.append({})

        self.mountpoint = None

        self.time = 0

    def assign(self, mountpoint):
        self.mountpoint = mountpoint
        self.x = mountpoint.x
        self.y = mountpoint.y

        mountpoint.arm = self

    def exec_task(self, task):
        for point in task.points:
            self.go_to_point(point)

        task.solved = True
        self.tasks.append(task)

    def execute_all_tasks(self):
        next_task = self.find_best_next_task()

        while next_task is not None:
            self.exec_task(next_task)

            next_task = self.find_best_next_task()

    def find_best_next_task(self):
        best = None
        best_score = -99999
        
        for task in self.O.tasks:
            (score, moves) = task.get_score_and_moves(self)

            if self.time + moves > self.O.L.steps_count:
                continue

            ratio = score / max(1, moves)

            if ratio > best_score:
                best = task
                best_score = ratio

        return best

    def go_to_point(self, point: Point):
        while self.x != point.x:
            instruction = Instruction(self.O, self, self.x, self.y, self.x + np.sign(self.x - point.x), self.y)
            self.exec_instruction(instruction)
        while self.y != point.y:
            instruction = Instruction(self.O, self, self.x, self.y, self.x, self.y + np.sign(self.y - point.y))
            self.exec_instruction(instruction)

    def exec_instruction(self, instruction: Instruction):
        self.instructions.append(instruction)
        self.x = instruction.x2
        self.y = instruction.y2
        self.blocked.append({'x': instruction.x2, 'y': instruction.y2})

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ARM%03s(%-03s/%03s)" % (self.No, self.x, self.y)
