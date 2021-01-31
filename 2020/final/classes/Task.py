from . import Optimizer
from .Arm import Arm

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder


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
            path = self._get_moves(current_loc_x, current_loc_y, point.x, point.y)
            if path is None:
                return None

            steps_needed += len(path)

            current_loc_x = point.x
            current_loc_y = point.y

        return self.score, steps_needed

    def get_score_per_moves(self, arm: Arm):
        result = self.get_score_and_moves(arm)
        if result is None:
            return -1

        (score, moves) = result
        if moves == 0:
            moves = 1

        return score / moves

    def get_moves(self, arm):
        path = []
        current_loc_x = arm.x
        current_loc_y = arm.y

        for point in self.points:
            result = self._get_moves(current_loc_x, current_loc_y, point.x, point.y)
            if result is None:
                return None

            path += result

            current_loc_x = point.x
            current_loc_y = point.y

        return path

    def _get_moves(self, start_x, start_y, end_x, end_y):
        if start_x == end_x and start_y == end_y:
            return []

        start_value = self.O.L.map[start_y][start_x]
        end_value = self.O.L.map[start_y][start_x]
        self.O.L.map[start_y][start_x] = 1
        self.O.L.map[start_y][start_x] = 1

        grid = Grid(matrix=self.O.L.map)
        start = grid.node(start_x, start_y)
        end = grid.node(end_x, end_y)
        finder = AStarFinder(diagonal_movement=DiagonalMovement.never)
        path, runs = finder.find_path(start, end, grid)
        grid.cleanup()

        self.O.L.map[start_y][start_x] = start_value
        self.O.L.map[start_y][start_x] = end_value

        if len(path) == 0:
            return None

        return path
