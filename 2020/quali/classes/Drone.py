import math
from heapq import *

class Drone:
    CNTR = 0

    def __init__(self, O):
        self.x = 0
        self.y = 0
        self.T = 0
        self.O = O
        self.actions = []

        self.finished = False

        self.No = Drone.CNTR
        Drone.CNTR += 1

    def findBestAction(self):
        (warehouse, actionSeq) = self.findBestWarehouse()

        if (warehouse is None):
            self.finished = True
        else:
            self.execActions(actionSeq)

    def dist(self, o1, o2):
        return math.ceil(math.sqrt(((o1.x - o2.x)**2 + (o1.y - o2.y)**2)))

    '''(warehouse, order)'''
    def findBestWarehouseOrder(self):
        warehouseQ = []

        best = None
        bestOrder = None
        bestScore = 0
        bestEnd = 99999999999

        for warehouse in self.O.warehouses:
            heappush(warehouseQ, (self.dist(warehouse, self), warehouse))

        while len(warehouseQ) > 0:
            (dist, warehouse) = heappop(warehouseQ)

            if (bestEnd < dist):
                break

            # print("New WH:", warehouse, dist)
            (score, order, endTime) = warehouse.getBestOrder(self)

            if order is None:
                continue

            if (score > bestScore):
                best = warehouse
                bestEnd = endTime
                bestScore = score
                bestOrder = order
                # print("  New best:", warehouse, order, endTime, score)

            # print("")

        if (best is None or bestOrder is None):
            self.finished = True

        return (best, bestOrder)

    def execActions(self, sequence):
        pass

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)
    def __str__(self):
        return "DRONE%03s(%-04s, %-04s, %-05s)" % (self.No, self.x, self.y, self.T)
