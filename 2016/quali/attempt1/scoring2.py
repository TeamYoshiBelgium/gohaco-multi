import math

class Settings:
    turns = 0
    load = 0

class Wrapper:
    drones = []
    warehouses = []
    products = []
    orders = []

class Product:
    CNTR = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "P" + str(self.No)

    def __init__(self, weight):
        self.weight = weight

        self.No = Product.CNTR
        Product.CNTR += 1

class Warehouse:
    CNTR = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "W" + str(self.No)

    def __init__(self, x, y, stock):
        self.x = x
        self.y = y
        self.stock = stock

        self.No = Warehouse.CNTR
        Warehouse.CNTR += 1

class Order:
    CNTR = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "O" + str(self.No)

    def __init__(self, x, y, products):
        self.x = x
        self.y = y

        self.products = products
        self.finished = False
        self.finishTime = 0

        self.No = Order.CNTR
        Order.CNTR += 1

class Drone:
    CNTR = 0

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "D" + str(self.No)

    def __init__(self):
        self.No = Drone.CNTR
        Drone.CNTR += 1

        self.x = 0
        self.y = 0

        self.T = 0

        self.products = []
        self.weight = 0

    def travel(self, x, y):
        self.T += math.ceil(
            math.sqrt(
                (self.x - x)**2 +
                (self.y - y)**2
            )
        )

        if (self.T > Settings.turns):
            raise Exception(
                str("Drone %d exceeded its max time " +
                "whilst moving from (%d, %d) to (%d, %d)." +
                " End time: %d, turns: %d") % (self.No, self.x, self.y, x, y, self.T, Settings.turns)
            )

        self.x = x
        self.y = y

    def performLoad(self, warehouse, product, quantity):
        print("Load", self.weight, product, quantity, product.weight * quantity)
        if (self.x != warehouse.x or self.y != warehouse.y):
            self.travel(warehouse.x, warehouse.y)

        self.T += 1
        self.weight += product.weight * quantity

        if (self.T > Settings.turns):
            raise Exception(
                str("Drone %d exceeded its max time " +
                "whilst loading a product at (%d, %d, %s) ." +
                " End time: %d, turns: %d") % (self.No, self.x, self.y, warehouse, self.T, Settings.turns)
            )

        if (self.weight > Settings.load):
            raise Exception(
                str("Drone %d exceeded its load capacity " +
                "whilst loading product %s (%d) at (%d, %d, %s) ." +
                " End weight: %d, max: %d") % (self.No, product, product.weight, self.x, self.y, warehouse, self.weight, Settings.load)
            )

        warehouse.stock[product.No] -= quantity
        # if (warehouse.stock[product.No] < 0):
        #     raise Exception(
        #         str("Drone %d exhausted the products of type " +
        #         "%s (%d) at warehouse (%d, %d, %s) ." +
        #         " End stock: %d, begin stock: %d") % (self.No, product, product.weight, warehouse.x, warehouse.y, warehouse, warehouse.stock[product.No], warehouse.stock[product.No] + quantity)
        #     )

        for i in range(quantity):
            self.products.append(product)

    def performUnload(self, warehouse, product, quantity):
        print("Unload", self.weight, product, quantity, product.weight * quantity)
        if (self.x != warehouse.x or self.y != warehouse.y):
            self.travel(warehouse.x, warehouse.y)

        self.T += 1
        self.weight -= product.weight * quantity

        if (self.T > Settings.turns):
            raise Exception(
                str("Drone %d exceeded its max time " +
                "whilst unloading a product at (%d, %d, %s) ." +
                " End time: %d, turns: %d") % (self.No, self.x, self.y, warehouse, self.T, Settings.turns)
            )

        for i in range(quantity):
            if product not in self.products:
                raise Exception(
                    str("Drone %d tried to unload product " +
                    "%s (%d) at (%d, %d, %s), whilst" +
                    "it is not present in its inventory: %s") % (self.No, product, product.weight, self.x, self.y, warehouse, self.products)
                )

            self.products.remove(product)

        warehouse.stock[product.No] += quantity

    def performDeliver(self, order, product, quantity):
        print("Deliver", self.weight, product, quantity, product.weight * quantity)
        if (self.x != order.x or self.y != order.y):
            self.travel(order.x, order.y)

        self.T += 1
        self.weight -= product.weight * quantity

        if (self.T > Settings.turns):
            raise Exception(
                str("Drone %d exceeded its max time " +
                "whilst unloading a product at (%d, %d, %s) ." +
                " End time: %d, turns: %d") % (self.No, self.x, self.y, order, self.T, Settings.turns)
            )

        for i in range(quantity):
            if product not in self.products:
                raise Exception(
                    str("Drone %d tried to unload product " +
                    "%s (%d) at (%d, %d, %s), whilst" +
                    "it is not present in its inventory: %s") % (self.No, product, product.weight, self.x, self.y, order, self.products)
                )

            if product not in order.products:
                raise Exception(
                    str("Drone %d tried to unload product " +
                    "%s (%d) at (%d, %d, %s), whilst" +
                    "it is not in demand at this order: %s") % (self.No, product, product.weight, self.x, self.y, order, order.products)
                )

            self.products.remove(product)
            order.products.remove(product)

        order.finishTime = max(order.finishTime, self.T)
        if (len(order.products) == 0):
            order.finished = True

    def performWait(self, turns):
        self.T += turns

class Reader:
    def __init__(self, inFile, outFile):
        self.inFile = inFile
        self.outFile = outFile

    def readInput(self):
        with open(self.inFile) as file:
            # Headerline
            rows, cols, droneCnt, turns, load = list(map(int, file.readline().strip().split(" ")))
            for i in range(droneCnt):
                Wrapper.drones.append(Drone())

            Settings.turns = turns
            Settings.load = load

            # Product count
            productCnt = int(file.readline().strip())

            # Products
            weights = list(map(int, file.readline().strip().split(" ")))
            assert len(weights) == productCnt

            for weight in weights:
                Wrapper.products.append(Product(weight))

            # WH count
            warehouseCnt = int(file.readline().strip())

            # Warehouses
            for i in  range(warehouseCnt):
                x, y = list(map(int, file.readline().strip().split(" ")))
                whProducts = list(map(int, file.readline().strip().split(" ")))
                assert len(whProducts) == productCnt
                Wrapper.warehouses.append(Warehouse(x,y,whProducts))

            # Order count
            orderCnt = int(file.readline().strip())

            # Orders
            for i in  range(orderCnt):
                x, y = list(map(int, file.readline().strip().split(" ")))

                ordProductCnt = int(file.readline().strip())

                ordProducts = list(map(int, file.readline().strip().split(" ")))
                ordProducts = list(map(lambda prod: Wrapper.products[prod], ordProducts))

                assert(ordProductCnt == len(ordProducts))

                Wrapper.orders.append(Order(x,y,ordProducts))

        print( "DRONES:     " , len(Wrapper.drones))
        print( "WAREHOUSES: " , len(Wrapper.warehouses))
        print( "ORDERS:     " , len(Wrapper.orders))
        print( "PRODUCTS:   " , len(Wrapper.products))
        print("===================================")
        return self

    def readOutput(self):
        def parseChar(char):
            if (char in ['L', 'U', 'D', 'W']):
                return char
            else:
                return int(char)
        i = 0
        try:

            with open(self.outFile) as file:
                # actionCnt
                i += 1
                actionCount = int(file.readline().strip())

                # actions
                for action in range(actionCount):
                    i += 1
                    params = list(map(parseChar, file.readline().strip().split(" ")))

                    drone = Wrapper.drones[params[0]]

                    if params[1] == 'U':

                        assert len(params) == 5

                        warehouse = Wrapper.warehouses[params[2]]
                        product = Wrapper.products[params[3]]
                        quantity = params[4]

                        drone.performUnload(warehouse, product, quantity)

                    elif params[1] == 'L':

                        assert len(params) == 5

                        warehouse = Wrapper.warehouses[params[2]]
                        product = Wrapper.products[params[3]]
                        quantity = params[4]

                        drone.performLoad(warehouse, product, quantity)

                    elif params[1] == 'D':

                        assert len(params) == 5

                        order = Wrapper.orders[params[2]]
                        product = Wrapper.products[params[3]]
                        quantity = params[4]

                        drone.performDeliver(order, product, quantity)

                    elif params[1] == 'W':

                        drone.performWait(params[2])

                    else:
                        raise Exception("Unknown action")

            score = 0
            for order in Wrapper.orders:
                if (order.finished is True):
                    score += math.ceil((Settings.turns - order.finishTime) / Settings.turns * 100)

            print("===================================")
            print("Score: ", score)
        except Exception as e:
            print(str(e))
            print("At line", i)

        return self

# Reader("in/busy_day.in", "out/busy_day.102394.out").readInput().readOutput()
# Reader("in/busy_day.in", "out/busy_day.103388.out").readInput().readOutput()
Reader("in/mother_of_all_warehouses.in", "out/mother_of_all_warehouses.75058.out").readInput().readOutput()
# Reader("in/redundancy.in", "out/redundancy.96754.out").readInput().readOutput()
# Reader("in/redundancy.in", "out/redundancy.96791.out").readInput().readOutput()
