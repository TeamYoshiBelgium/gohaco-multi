from . import Arm

class Instruction:
    CNTR = 0

    def __init__(self, optimizer, arm : Arm, x1: int, y1: int, x2: int, y2: int):
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
        return "INSTR%03s(%-03s/%03s)" % (self.No, self.x, self.y)
