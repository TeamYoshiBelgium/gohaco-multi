import math
import copy
from .Action import *

class Writer:
    def __init__(self, L, suffix=""):
        self.L = L
        self.suffix = suffix

    def write(self):
        score = 0
        rowObjects = []

        for scoringObject in :
            rowObjects += scoringObject

        filename = self.L.filename.replace(".in", "." + str(score) + self.suffix + ".out").replace("in/", "out/")

        with open(filename, 'w+') as file:
            file.write(str(len(rowObjects)) + '\n')

            for rowObject in rowObjects:
                file.write(rowObject.toString() + '\n')

        print(self.L.filename, "=>", filename)

        print("SCORE:", score)
