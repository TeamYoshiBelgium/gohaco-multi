from .Optimizer import Optimizer


class Product:
    CNTR = 0

    def __init__(self, optimizer: Optimizer, weight):
        self.O = optimizer

        self.weight = weight
        self.No = Product.CNTR
        Product.CNTR += 1

    def __repr__(self):
        return str(self)
    def __str__(self):
        return "PROD(%-03s)" % (self.weight)
