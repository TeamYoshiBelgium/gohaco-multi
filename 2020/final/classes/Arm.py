from math import copysign

import numpy as np

from .Instruction import Instruction
from .Optimizer import Optimizer
from .Task import Task
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

    def assign(self, mountpoint):
        self.mountpoint = mountpoint
        self.x = mountpoint.x
        self.y = mountpoint.y

        mountpoint.arm = self

    def exec_task(self, task: Task):
        for point in task.points:
            self.go_to_point(point)

        task.solved = True
        self.tasks.append(task)

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
