import random

class Video:
    CNTR = 0

    def __init__(self, Optimizer, size):
        self.O = Optimizer
        self.No = Video.CNTR
        self.size = size
        self.endpoints = []

        Video.CNTR += 1

        self.cachedServers = set()

    def findBestServer(self, limit):
        bestServer = None
        bestScore = 0
        random.shuffle(self.O.servers)
        serversChecked  = 0

        for server in self.O.servers:
            if server in self.cachedServers:
                continue
            if server.fill + self.size > server.maxSize:
                continue

            score = server.getScore(self)
            if (score > bestScore):
                bestScore = score
                bestServer = server

            serversChecked +=1

            if serversChecked >= limit:
                break

        return (bestScore, bestServer)

    def addServer(self, server):
        self.cachedServers.add(server)

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "VID%03s(%d)" % (self.No, self.size)

