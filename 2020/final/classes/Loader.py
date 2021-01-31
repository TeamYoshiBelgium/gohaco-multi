from .Optimizer import Optimizer
from .MountPoint import MountPoint
from .Task import Task
from .Point import Point


class Loader:
    def __init__(self, filename): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.map = []
        self.filename = filename
        self.O = Optimizer(self)  # heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim)

        with open(filename) as file:
            self.read_header_line(file)
            self.read_mount_points(file)
            self.read_tasks(file)

        self.O.init()

        pass

    def read_header_line(self, file):
        row = file.readline().split(" ")

        self.maps_width = int(row[0])
        self.maps_high = int(row[1])
        self.arms_count = int(row[2])
        self.mount_points_count = int(row[3])
        self.tasks_count = int(row[4])
        self.steps_count = int(row[5])
        pass

    def read_mount_points(self, file):
        self.mount_points = []
        for id in range(self.mount_points_count):
            row = file.readline().split(" ")
            x = int(row[0])
            y = int(row[1])
            mount_point = MountPoint(self.O, id, x, y)
            self.mount_points.append(mount_point)

        pass

    def read_tasks(self, file):
        self.tasks = []
        for id in range(self.tasks_count):
            row = file.readline().split(" ")
            score = int(row[0])
            points_count = int(row[1])
            task = Task(self.O, id, score, points_count)
            row = file.readline().split(" ")
            for point_id in range(points_count):
                x = int(row[point_id + 0])
                y = int(row[point_id + 1])
                point = Point(self.O, point_id, x, y)
                task.points.append(point)
            self.tasks.append(task)

        pass