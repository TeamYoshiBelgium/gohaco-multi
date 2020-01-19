from heapq import *
from tqdm import tqdm
from copy import copy

from .Drone import Drone

class Optimizer:
    def __init__(self):
        pass

    def init(self, Loader, products, warehouses, orders):
        self.products = products
        self.warehouses = warehouses
        self.orders = orders
        self.L = Loader
        self.drones = []

        for i in range(self.L.drones):
            self.drones.append(Drone(self))

    def preprocess(self):
        heap = []

        for order in self.orders:
            order.realInit()
        for warehouse in self.warehouses:
            warehouse.realInit()

        print("Generating distance queues...", flush=True)

        for order in self.orders:
            order.calculateDistances()

        for order in tqdm(self.orders):
            for i in range(len(order.orders)):
                pair = order.orders[i]

                if (pair is None):
                    continue

                if (order.No == pair[1].No):
                    continue

                val = []
                if (pair[1].No < order.No):
                    val.append(pair[1])
                    val.append(order)
                else:
                    val.append(order)
                    val.append(pair[1])

                heappush(heap, (pair[0], val))
                pair[1].orders[order.No] = None
                order.orders[i] = None

            for j in range(len(order.warehouses)):
                pair = order.warehouses[j]
                heappush(heap, (pair[0], [pair[1], order]))

        for warehouse in self.warehouses:
            warehouse.orders = []

        for order in self.orders:
            order.orders = []
            order.warehouses = []

        for pair in heap:
            if (pair[1][0].getType() == 'WH'):
                pair[1][0].orders.append(pair[1][1])
                pair[1][1].warehouses.append(pair[1][0])
            else:
                order1 = pair[1][0]
                order2 = pair[1][1]

                if (order1.weight + order2.weight <= self.L.load):
                    order1.orders.append(order2)
                    order2.orders.append(order1)

        print("Distance queues generated!", flush=True)

        print("", flush=True)

        print("Calculating surplus of WH...", flush=True)

        for wh in tqdm(self.warehouses):
            for product in self.products:
                wh.calculateProductSurplus(product)

        print("Surplus calculated.", flush=True)

        print("", flush=True)
        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):
        self.preprocess()

        droneQ = [ (drone.T, drone) for drone in self.drones ]

        drone = self.drones[0]
        # for warehouse in self.warehouses:
        #     print(warehouse, drone.dist(warehouse, drone), warehouse.orders[:3])

        # print("")

        i = 0
        while len(droneQ) > 0:
            (T, drone) = heappop(droneQ)
            (warehouse, order) = drone.findBestWarehouseOrder()
            # print(warehouse, order)

            if (i % 10 == 0):
                print(i, drone, drone.T, flush=True)

            i += 1

            if (drone.finished is not True):
                warehouse.executeOrderActions(drone, order)
                heappush(droneQ, (drone.T, drone))
                # break

        # print(self.drones[0].actions)
        finished = 0
        for order in self.orders:
            if (order.finished is True):
                finished += 1

        print("Finished:   ", finished)
        print("Unfinished: ", len(self.orders) - finished)


