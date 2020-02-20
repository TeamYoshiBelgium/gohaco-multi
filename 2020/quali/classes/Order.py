import math
import copy

from .Optimizer import Optimizer


class Order:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, x, y, products):
        self.O = optimizer

        self.x = int(x)
        self.y = int(y)

        self.products = products
        self.weight = sum([ x.weight for x in products ])
        self.productsRemaining = copy.copy(products)

        self.finished = False
        self.minFinish = 0
        self.finishTime = 0

        self.No = Order.CNTR
        Order.CNTR += 1

    def realInit(self):
        self.orders = [None] * len(self.O.orders)
        self.warehouses = [None] * len(self.O.warehouses)
        self.productsRemaining = sorted(
            self.productsRemaining,
            key=lambda product: product.weight - 0.5 * product.No / len(self.O.products), reverse=True
        )

    def getType(self):
      return 'OR'

    def dist(self, o1, o2):
        return math.ceil(math.sqrt(((o1.x - o2.x)**2 + (o1.y - o2.y)**2)))

    def calculateDistances(self):
        for i in range(len(self.O.orders)):
            if (self.orders[i] is not None):
                continue

            other = self.O.orders[i]
            dist = self.dist(self, other)
            self.orders[i] = (dist, other)
            other.orders[self.No] = (dist, self)

        for i in range(len(self.O.warehouses)):
            other = self.O.warehouses[i]
            dist = self.dist(self, other)
            self.warehouses[i] = (dist, other)
            other.orders[self.No] = (dist, self)

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "ORDR(%-03s|%-03s, %s: %s)" % (self.x, self.y, len(self.products), self.weight)
