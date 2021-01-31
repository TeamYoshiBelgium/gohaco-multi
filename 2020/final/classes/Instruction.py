from . import Arm
from . import Optimizer


class Instruction:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, arm: Arm, x1: int, y1: int, x2: int, y2: int):
        self.O = optimizer
        self.No = Instruction.CNTR
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.arm = arm

        if abs(x1-x2) > 1 or abs(y1-y2) > 1:
            print("ERROR: instructions unclear :) diff > 1 (%d,%d,%d,%d)" % (x1,x2,y1,y2))


    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.__move__()

    def __move__(self):
        if self.x1-self.x2 > 0:
            return "L"
        elif self.x1-self.x2 < 0:
            return "R"
        elif self.y1-self.y2 > 0:
            return "D"
        elif self.y1-self.y2 < 0:
            return "U"
        else:
            return "W"
