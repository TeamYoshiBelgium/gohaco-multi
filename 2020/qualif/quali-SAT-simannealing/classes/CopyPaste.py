import math
from heapq import *

class CopyPaste:
    CNTR = 0

    def __init__(self, O):
        self.O = O

        self.No = Drone.CNTR
        Drone.CNTR += 1
