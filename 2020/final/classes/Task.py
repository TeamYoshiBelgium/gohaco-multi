from . import Optimizer
from .Arm import Arm
import math

class Task:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, id, score, points_count):
        self.O = optimizer
        self.id = id
        self.score = score
        self.points_count = points_count
        self.points = []

        self.No = id

        self.solved = False
        self.arm = None

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "TASK%03s(%-03s/%03s)" % (self.No, self.score, self.points_count)

    def get_score_and_moves(self, arm: Arm):
        current_loc_x = arm.x
        current_loc_y = arm.y
        steps_needed = 0

        for point in self.points:
            distance_x = math.abs(current_loc_x - point.x)
            distance_y = math.abs(current_loc_y - point.y)

            steps_needed += distance_x + distance_y

            current_loc_x = point.x
            current_loc_y = point.y

        return (self.score, steps_needed)

    def get_score_per_moves(self, arm: Arm):
        (score, moves) = self.get_score_and_moves(self, arm)
        if moves == 0:
            moves = 1

        return score / moves
