import random
from heapq import *

class Video:
    CNTR = 0

    def __init__(self, Optimizer, size):
        self.O = Optimizer
        self.No = Video.CNTR
        self.size = size
        self.endpoints = set()
        self.servers = set()

        Video.CNTR += 1

        self.cachedServers = set()
        self.orderedServers = []

    def findBestServer(self):
        for pair in self.orderedServers:
            server = pair[1]

            if server in self.cachedServers:
                raise Exception("Wut, server should not be in ordered if cached... %s %s %s %s" % (self, server, self.cachedServers, self.servers))

            if server.fill + self.size > server.maxSize:
                continue

            return (pair[0], server)

        return (None, None)


    def calcBestServers(self):
        self.orderedServers = []
        heap = []
        for server in self.servers:
            if server in self.cachedServers:
                continue
            if server.fill + self.size > server.maxSize:
                continue

            score = server.getScore(self)
            heappush(heap, (-score, server))

        if (len(heap) == 0):
            # print("%s FINISHED" % self)
            self.O.videos.remove(self)
            self.orderedServers = []
        else:
            for pair in heap:
                self.orderedServers.append((-pair[0], pair[1]))


    def addServer(self, server):
        self.cachedServers.add(server)
        self.calcBestServers()

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "VID%03s(%d)" % (self.No, self.size)

