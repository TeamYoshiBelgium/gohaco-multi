from classes import Optimizer, Loader


class Writer:
    def __init__(self, L: Loader, O: Optimizer):
        self.L = L
        self.O = O

    def write(self):
        score = 0

        for car in self.L.O.cars:
            score += car.get_score()

        filename = self.L.filename.replace(".in", "." + str(score) + ".out").replace("in/", "out/")
        # filename = filename.replace(".out", ".NEW.out")
        # filename = filename.replace(".out",
        #     "." +
        #     str(self.L.O.heuristic_signup) + "-" +
        #     str(self.L.O.heuristic_wasted) + ".out"
        # )

        # filename = filename.replace(".out",
        #     "." +
        #     str(self.L.O.heuristic_useless) + "-" +
        #     str(self.L.O.heuristic_signup) + "-" +
        #     str(self.L.O.heuristic_bookcount) + "-" +
        #     str(self.L.O.heuristic_realdays) + "-" +
        #     str(self.L.O.trim) + ".out"
        # )

        with open(filename, 'w+') as file:
            file.write(str(len(self.L.O.intersections)))
            file.write("\n")
            for intersection in self.L.O.intersections:
                file.write(str(intersection.id))
                file.write("\n")
                file.write(str(len(intersection.streets)))
                for street in intersection.streets:
                    file.write(str(street.name) + " " + str(street.green))
                file.write("\n")
