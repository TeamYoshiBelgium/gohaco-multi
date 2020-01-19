import math
import copy

from .Optimizer import Optimizer
from .Action import *

class Warehouse:
    CNTR = 0
    def __init__(self, optimizer: Optimizer, x, y):
        self.O = optimizer

        self.x = x
        self.y = y
        self.stock = []
        self.arrivals = []
        self.orders = []
        self.surplus = []

        self.No = Warehouse.CNTR
        Warehouse.CNTR += 1

    def getType(self):
      return 'WH'

    def realInit(self):
      self.orders = [None] * len(self.O.orders)
      self.surplus = [None] * len(self.O.products)

    def initStock(self, item):
        self.stock.append(item)

    '''(score, order, finish)'''
    def getBestOrder(self, drone):
        bestTime = 9999999999999
        bestScore = 0
        bestOrder = None

        if (drone.T + drone.dist(self, drone) + 1 > self.O.L.turns):
            return (None, None)

        for order in self.orders:
            if (order.finished):
                continue

            if (drone.T + drone.dist(self, drone) + len(order.productsRemaining) * 2 > self.O.L.turns):
                break

            # Simplification (best order currently has a better total time than a one-way to the order)
            # This order might still be better however (unlikely)
            if (bestTime < drone.dist(self, drone)):
                continue

            (productsAvailable, weight) = self.claimProducts(order)
            self.restoreProducts(order)

            # simplification => multiple + parallel
            if productsAvailable is False:
                # Nothing to find here
                if weight == 0:
                    continue

                elligibleProducts = []
                totalRemainingWeight = 0
                for product in order.productsRemaining:
                    totalRemainingWeight += product.weight
                    if self.stock[product.No] > 0:
                        elligibleProducts.append(product)
                        self.stock[product.No] -= 1

                if (len(elligibleProducts) == 0):
                    continue

                for product in elligibleProducts:
                    self.stock[product.No] += 1

                fill = self.getOptimalFill(elligibleProducts)
                weight = 0
                for product in fill:
                    weight += product.weight

                time = drone.T
                time += drone.dist(self, drone)

                # simplification: double products
                time += len(fill)
                time += drone.dist(self, order)

                time += len(fill)

                score = (self.O.L.turns - time) / self.O.L.turns * 100
                score = score / 1.5 # Absolute penalty for no fullfill
                score *= (weight / totalRemainingWeight) # relative penalty for no fulfill

            elif (weight <= self.O.L.load):
                time = drone.T
                time += drone.dist(self, drone)

                # simplification: double products
                time += len(order.productsRemaining)

                time += drone.dist(self, order)

                time += len(order.productsRemaining)

                #simplification: piggybacking?

                score = (self.O.L.turns - time) / self.O.L.turns * 100
            else:
                time = drone.T
                time += drone.dist(self, drone)

                # simplification: double products
                time += len(order.productsRemaining)

                # simplification => parallel drones
                # simplification => ignoring drone load distribution
                time += 2 * (math.ceil(weight/self.O.L.load) - 1) * drone.dist(self, order) + drone.dist(self, order)

                # simplification: double products
                time += len(order.productsRemaining)

                # simplification => parallel drones
                if (time > self.O.L.turns):
                    continue

                score = (self.O.L.turns - time) / self.O.L.turns * 100

            # Simplification, score 100 might be regardless of weight, include weight factor after rounding
            # piggyScore = math.floor((1 - (math.ceil(origScore) - origScore))*self.O.L.turns)/self.O.L.turns

            score -= 0.1
            # Simplification: probably piggybaggable
            if ((self.O.L.load - weight)/weight > 0.5):
                score += 0.1

            if (score > bestScore):
                # print("     New best order:", score, order, time)
                bestScore = score
                bestTime = time
                bestOrder = order
            # else:
                # print("     worse: ", score, order)
        return (bestScore, bestOrder, bestTime)

    def claimProducts(self, order):
        productsAvailable = True
        weight = 0
        for product in order.productsRemaining:
            if (self.stock[product.No] == 0):
                productsAvailable = False
            else:
                weight += product.weight

            self.stock[product.No] -= 1

        return (productsAvailable, weight)

    def restoreProducts(self, order):
        for product in order.productsRemaining:
            self.stock[product.No] += 1

    def executeOrderActions(self, drone, order):
        (productsAvailable, weight) = self.claimProducts(order)
        self.restoreProducts(order)

        if (productsAvailable is False):
            elligibleProducts = []
            for product in order.productsRemaining:
                if self.stock[product.No] > 0:
                    elligibleProducts.append(product)
                    self.stock[product.No] -= 1

            for product in elligibleProducts:
                self.stock[product.No] += 1

            optimalFill = self.getOptimalFill(elligibleProducts)
            products = {}
            for product in optimalFill:
                if (product not in products):
                    products[product] = 0

                products[product] += 1

            self.performLoadingActions(drone, order, products)
        else:
            products = {}
            for product in order.productsRemaining:
                if (product not in products):
                    products[product] = 0
                products[product] += 1

            if (weight < self.O.L.load / 2):
                piggy = None
                for piggyback in order.orders:
                    if piggyback.finished:
                        continue

                    if drone.dist(order, piggyback) > drone.dist(piggyback, piggyback.warehouses[0]):
                        continue

                    pigWeight = 0
                    for product in piggyback.productsRemaining:
                        pigWeight += product.weight
                        self.stock[product.No] -= 1
                        if (self.stock[product.No] < 0):
                            pigWeight = 999999999999

                    for product in piggyback.productsRemaining:
                        self.stock[product.No] += 1

                    # Simplification, might still be worth it
                    # to deliver incomplete load
                    if (weight + pigWeight > self.O.L.load):
                        continue

                    piggy = piggyback
                    break
                if piggy is None:

                    if order.warehouses[0] != self:

                        self.claimProducts(order)
                        for product in order.productsRemaining:
                            self.calculateProductSurplus(product)
                        #TODO piggybacking to a warehouse
                        # using self.surplus
                        piggyWH = {}
                        wh = order.warehouses[0]
                        for product in self.O.products:
                            no = product.No

                            if self.O.L.load - weight < product.weight:
                                continue

                            if self.surplus[no] < 0:
                                continue

                            if wh.surplus[no] > 0:
                                continue

                            if self.surplus[no] > wh.surplus[no]:
                                piggyWH[product] = (self.surplus[no] - wh.surplus[no]) / product.weight

                        self.restoreProducts(order)
                        for product in order.productsRemaining:
                            self.calculateProductSurplus(product)

                        piggyWHsorted = sorted(piggyWH.keys(), key=lambda i: piggyWH[i])
                        if (piggyWHsorted is not None and len(piggyWHsorted) > 0):
                            self.performPiggyWarehouseActions(drone, order, products, piggyWHsorted)
                        else:
                            print("NO PIGGY WH PRODUCTS!!!", flush=True)
                            self.performLoadingActions(drone, order, products)
                    else:
                        self.performLoadingActions(drone, order, products)
                else:
                    self.performPiggyOrderActions(drone, order, products, piggy)
            else:
                optimalFill = self.getOptimalFill(order.productsRemaining)
                products = {}
                for product in optimalFill:
                    if (product not in products):
                        products[product] = 0

                    products[product] += 1

                self.performLoadingActions(drone, order, products)

    def calculateProductSurplus(self, product):
        needed = 0
        for order in self.orders[:100]:
            if order.finished is True:
                continue

            closestWhRank = 1
            if product in order.productsRemaining:
                for warehouse in order.warehouses[:4]:
                    if warehouse == self:
                        break

                    if warehouse.stock[product.No] > 0:
                        closestWhRank *= 2

                needed += 1/closestWhRank

        self.surplus[product.No] = self.stock[product.No] - needed

    def performPiggyWarehouseActions(self, drone, order, productsMap, piggyProductsSorted):
        weight = sum([ productsMap[product] * product.weight for product in productsMap ])
        fullMap = copy.copy(productsMap)
        additional = {}

        print("PIGGYBACKING WH: ", drone, order, end="")

        for product in piggyProductsSorted:
            if self.O.L.load - weight >= product.weight:
                weight += product.weight

                if product not in fullMap:
                    fullMap[product] = 0

                fullMap[product] += 1

                if product not in additional:
                    additional[product] = 0

                additional[product] += 1

            if (weight == self.O.L.load):
                break

        print(", weight=", sum([ fullMap[product] * product.weight for product in fullMap ]), end=" ")
        print(additional, flush=True)

        loadingTurns = len(list(fullMap))
        unloadingOrderTurns = len(list(productsMap))
        unloadingWarehouseTurns = len(list(additional))

        T = drone.T
        T += drone.dist(self, drone)
        T += loadingTurns
        T += drone.dist(self, order)
        T += unloadingOrderTurns
        finishT = T
        T += drone.dist(order, order.warehouses[0])
        T += unloadingWarehouseTurns

        # Fuck redistribution at the end
        if (T >= self.O.L.turns*0.95):
            return self.performLoadingActions(drone, order, productsMap)

        drone.T = T

        drone.x = order.warehouses[0].x
        drone.y = order.warehouses[0].y

        for product in fullMap:
            drone.actions.append(LoadAction(self.O, drone, self, product, fullMap[product]))

            for i in range(fullMap[product]):
                self.stock[product.No] -= 1

            self.calculateProductSurplus(product)

        for product in productsMap:
            drone.actions.append(DeliverAction(self.O, drone, order, product, productsMap[product]))

            for i in range(productsMap[product]):
                order.productsRemaining.remove(product)


        for product in additional:
            drone.actions.append(UnloadAction(self.O, drone, order.warehouses[0], product, additional[product]))
            order.warehouses[0].stock[product.No] += additional[product]
            order.warehouses[0].calculateProductSurplus(product)

        if (len(order.productsRemaining) == 0):
            order.finished = True
            order.finishTime = max(finishT, order.minFinish)
        else:
            order.minFinish = max(order.minFinish, finishT)

    def performLoadingActions(self, drone, order, productsMap):
        loadingTurns = len(list(productsMap))
        drone.T += drone.dist(self, drone)
        drone.T += loadingTurns
        drone.T += drone.dist(self, order)
        drone.T += loadingTurns
        drone.x = order.x
        drone.y = order.y

        for product in productsMap:
            drone.actions.append(LoadAction(self.O, drone, self, product, productsMap[product]))

            for i in range(productsMap[product]):
                self.stock[product.No] -= 1
                order.productsRemaining.remove(product)

        for product in productsMap:
            drone.actions.append(DeliverAction(self.O, drone, order, product, productsMap[product]))
            self.calculateProductSurplus(product)

        if (len(order.productsRemaining) == 0):
            order.finished = True
            order.finishTime = max(drone.T, order.minFinish)
        else:
            order.minFinish = max(order.minFinish, drone.T)

    def performPiggyOrderActions(self, drone, order, productsMap, piggy):
        print("PIGGYBACKING ORDR: ", drone, order, piggy)
        loadMap = copy.copy(productsMap)
        unloadFirstMap = productsMap
        unloadSecondMap = {}

        for product in piggy.productsRemaining:
            if product not in productsMap:
                loadMap[product] = 0

            if product not in unloadSecondMap:
                unloadSecondMap[product] = 0

            loadMap[product] += 1
            unloadSecondMap[product] += 1

        drone.T += drone.dist(self, drone)
        drone.T += len(list(loadMap)) # Loading

        drone.T += drone.dist(self, order)
        drone.T += len(list(unloadFirstMap)) # Unloading 1
        firstT = drone.T

        drone.T += drone.dist(order, piggy)
        drone.T += len(list(unloadSecondMap)) # Unloading 2
        secondT = drone.T

        drone.x = piggy.x
        drone.y = piggy.y

        for product in loadMap:
            drone.actions.append(LoadAction(self.O, drone, self, product, loadMap[product]))

            for i in range(loadMap[product]):
                self.stock[product.No] -= 1

        for product in unloadFirstMap:
            order.productsRemaining.remove(product)
            drone.actions.append(DeliverAction(self.O, drone, order, product, unloadFirstMap[product]))

        for product in unloadSecondMap:
            piggy.productsRemaining.remove(product)
            drone.actions.append(DeliverAction(self.O, drone, piggy, product, unloadSecondMap[product]))

        for product in loadMap:
            self.calculateProductSurplus(product)

        if (len(order.productsRemaining) == 0):
            order.finished = True
            order.finishTime = max(firstT, order.minFinish)
        else:
            order.minFinish = max(order.minFinish, firstT)

        if (len(piggy.productsRemaining) == 0):
            piggy.finished = True
            piggy.finishTime = max(secondT, piggy.minFinish)
        else:
            piggy.minFinish = max(piggy.minFinish, secondT)

    def getOptimalFill(self, products):
        weight = 0
        fill = []

        # Greedy filling with weight based sorting:
        # First heavy,
        # Then light
        # Simplification: more optimal filling might exist!
        for product in products:
            if (weight + product.weight <= self.O.L.load):
                fill.append(product)
                weight += product.weight

        # print("  products:", products, fill)
        return fill

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)
    def __str__(self):
        return "WHSE(%-04s, %-04s)" % (self.x, self.y)
