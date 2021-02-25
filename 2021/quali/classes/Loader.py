from .Optimizer import Optimizer
from .Street import Street
from .Car import Car
from .Intersection import Intersection


class Loader:
    def __init__(self, filename, swap_vs_increment_heuristic, increment_decrement_heuristic): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer(self, swap_vs_increment_heuristic, increment_decrement_heuristic)#heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim)

            self.read_header_line(file)
            self.O.streets = self.read_streets(file)
            self.O.cars = self.read_cars(file)

            intersections = dict()
            for street in self.O.streets:
                if street.start not in intersections:
                    intersections[street.start] = [street.name]
                else:
                    intersections[street.start].append(street.name)
                if street.end not in intersections:
                    intersections[street.end] = [street.name]
                else:
                    intersections[street.end].append(street.name)

            self.O.intersections = []
            self.O.intersections_dict = dict()
            for key in intersections.keys():
                intersection = Intersection(self.O, key, intersections[key])
                self.O.intersections.append(intersection)
                self.O.intersections_dict[key] = intersection

            self.O.streets_dict = dict()
            for street in self.O.streets:
                self.O.streets_dict[street.name] = street

            for car in self.O.cars:
                car.streets_obj = []
                for street in car.streets:
                    car.streets_obj.append(self.O.streets_dict[street])

                car.streets_ids = car.streets
                car.streets = car.streets_obj

            for street in self.O.streets:
                street.start_intersection = self.O.intersections_dict[street.start]
                street.end_intersection = self.O.intersections_dict[street.end]

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

        for i in range(self.O.cars):
            row = file.readline()
            splitted = row.strip().split(" ")
            count = int(splitted[0])
            streets = splitted[1:]

            car = Car(self.O, count, streets)

            cars.append(car)

        return cars