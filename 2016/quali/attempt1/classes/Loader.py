
from .Product import Product
from .Warehouse import Warehouse
from .Order import Order
from .Optimizer import Optimizer


class Loader:
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer()

            self.readHeaderLine(file)
            self.readProductTypesLine(file)
            self.readProductWeightLine(file)
            self.readWarehouseCountLine(file)

            for i in range(self.warehouseCount):
                self.readWareHouse(file, i)

            self.readOrderCountLine(file)

            for i in range(self.orderCount):
                self.readOrder(file, i)

            print("FILE:        ", filename)
            print("Products:    ", len(self.products))
            print("Warehouses:  ", len(self.warehouses))
            print("Orders:      ", len(self.orders))
            print("Drones:      ", self.drones)
            print("Load:        ", self.load)
            print("Turns:       ", self.turns)
            print("")
            print("Total stock: ", self.productWarehouseCount)
            print("Total req:   ", self.orderProductCount)
            print("")

            self.O.init(self, self.products, self.warehouses, self.orders)
            self.O.optimize()

    def readHeaderLine(self, file):
        row = file.readline().split(" ")

        self.cols   = int(row[0])
        self.rows   = int(row[1])
        self.drones = int(row[2])
        self.turns  = int(row[3])
        self.load   = int(row[4])

    def readProductTypesLine(self, file):
        self.productCount = int(file.readline())
        self.products = [None]*self.productCount
        self.productWarehouseCount = 0
        self.orderProductCount = 0

    def readProductWeightLine(self, file):
        weights = file.readline().split(" ")
        i = 0
        for weight in weights:
            self.products[i] = Product(self.O, int(weight))

            i += 1

    def readWarehouseCountLine(self, file):
        self.warehouseCount = int(file.readline())
        self.warehouses = [None]*self.warehouseCount

    def readWareHouse(self, file, i):
        self.readWareHouseLocationLine(file, i)
        self.readWareHouseProductLine(file, i)

    def readWareHouseLocationLine(self, file, i):
        loc = file.readline().split(" ")
        self.warehouses[i] = Warehouse(self.O, int(loc[0]), int(loc[1]))

    def readWareHouseProductLine(self, file, i):
        counts = file.readline().split(" ")
        for count in counts:
            self.warehouses[i].initStock(int(count))
            self.productWarehouseCount += int(count)

    def readOrderCountLine(self, file):
        self.orderCount = int(file.readline())
        self.orders = [None]*self.orderCount

    def readOrder(self, file, i):
        location     = file.readline().split(" ")
        productCount = int(file.readline())
        products     = file.readline().split(" ")

        realProducts = []
        for product in products:
            realProducts.append(self.products[int(product)])
            self.orderProductCount += 1

        self.orders[i] = Order(self.O, int(location[0]), int(location[1]), realProducts)


