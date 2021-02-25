from .Optimizer import Optimizer
from .Street import Street
from .Car import Car


class Loader:
    def __init__(self, filename): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer(self)#heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim)

            self.read_header_line(file)
            self.O.streets = self.read_streets(file)
            self.O.cars = self.read_cars(file)

        pass

    def read_header_line(self, file):
        row = file.readline().split(" ")

        self.O.duration = int(row[0])
        self.O.intersections = int(row[1])
        self.O.streets = int(row[2])
        self.O.cars = int(row[3])
        self.O.score = int(row[1])
        pass

    def read_streets(self, file):
        streets = []

        for i in range(self.O.streets):
            row = file.readline()
            splitted = row.split(" ")
            start = int(splitted[0])
            end = int(splitted[1])
            name = splitted[2]
            time = int(splitted[3])

            street = Street(self.O, name, start, end, time)

            streets.append(street)

        return streets

    def read_cars(self, file):
        cars = []

        for i in range(self.streets):
            row = file.readline()
            splitted = row.split(" ")
            count = int(splitted[0])
            streets = splitted[1:]

            car = Car(self.O, count, streets)

            cars.append(car)

        return cars