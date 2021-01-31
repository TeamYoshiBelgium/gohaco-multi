from .Optimizer import Optimizer
from .MountPoint import MountPoint


class Loader:
    def __init__(self, filename, heuristic_signup, heuristic_wasted): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.map = []
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer(heuristic_signup, heuristic_wasted)#heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim)

            self.read_header_line(file)
            self.read_mount_points(file)
            self.read_tasks(file)

            # for library in self.libraries:
            #     print(len(library.books))

            filtered_books = list(filter(
                lambda book: not len(book.libraries) == 0,
                self.books
            ))

            self.O.books = filtered_books
            self.O.libraries = self.libraries
            self.O.max = self.days
        pass

    def read_header_line(self, file):
        row = file.readline().split(" ")

        self.maps_width = int(row[0])
        self.maps_high = int(row[1])
        self.arms_count = int(row[2])
        self.mount_points_count = int(row[3])
        self._tasks_count = int(row[4])
        self._steps_count = int(row[5])
        pass

    def read_mount_points(self, file):
        self.mount_points = []
        for id in len(self.mount_points_count):
            row = file.readline().split(" ")
            x = int(row[0])
            y = int(row[1])
            mount_point = MountPoint(self.O, id, x, y)
            self.mount_points.append(mount_point)

        pass

    def read_tasks(self, file):
        self.tasks = []
        for id in len(self.mount_points_count):
            row = file.readline().split(" ")
            x = int(row[0])
            y = int(row[1])
            mount_point = MountPoint(self.O, id, x, y)
            self.mount_points.append(mount_point)

        pass