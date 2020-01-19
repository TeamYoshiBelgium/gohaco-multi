import math
import copy

class Writer:
    def __init__(self, L, suffix=""):
        self.L = L
        self.suffix = suffix

    def write(self):
        score = 0

        rowObjects = []

        for scoringObject in self.L.O.servers:
            rowObjects += " ".join([ scoringObject.No ] + [ v.No for v in scoringObject.videos ])

        score = 0
        total = 0
        for request in self.L.O.requests:
            score += request.quantity * request.saved
            total += request.quantity

        score = score / total * 1000

        filename = self.L.filename.replace(".in", "." + str(score) + self.suffix + ".out").replace("in/", "out/")

        with open(filename, 'w+') as file:
            file.write(str(len(rowObjects)) + '\n')

            for rowObject in rowObjects:
                file.write(rowObject.toString() + '\n')

        print(self.L.filename, "=>", filename)

        print("SCORE:", score)
