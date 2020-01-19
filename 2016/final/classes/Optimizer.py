import copy
import random

from heapq import *
from tqdm import tqdm

from .Drone import Drone

class Optimizer:
    def __init__(self):
        pass

    def init(self, Loader, products, warehouses, orders):
        # self.products = products
        # self.warehouses = warehouses
        # self.orders = orders
        # self.L = Loader
        # self.drones = []

        # for i in range(self.L.drones):
        #     self.drones.append(Drone(self))

    def optimize(self):
        print("[OPT] Starting optimization", flush=True)

        print("[OPT] Finished")
