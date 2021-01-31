from . import Optimizer
from . import Loader


class Writer:
    def __init__(self, L: Loader, O: Optimizer):
        self.L = L
        self.O = O

    def write(self):
        score = 0
        for arm in self.L.O.robotic_arms:
            for task in arm.tasks:
                score += task.score

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
            file.write(str(len(self.L.O.robotic_arms)))
            file.write("\n")
            for arm in self.L.O.robotic_arms:
                file.write(str(arm.x) + " " + str(arm.y) + " " + str(len(arm.tasks)) + " " + str(len(arm.commands)))
                file.write("\n")
                for task in arm.tasks:
                    file.write(str(task.No) + " ")
                file.write("\n")
                for command in arm.commands:
                    file.write(str(command) + " ")
