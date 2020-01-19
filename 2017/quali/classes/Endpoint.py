class Endpoint:
    CNTR = 0

    def __init__(self, Optimizer, latency, cacheServers):
        self.O = Optimizer
        self.No = Endpoint.CNTR

        self.latency = latency
        self.cacheServers = cacheServers
        self.cacheCnt = len(cacheServers)

        self.requests = []
        self.videosRequestsMap = {}
        self.videosLatencyMap = {}
        self.videosCountMap = {}

        Endpoint.CNTR += 1

        for server in self.cacheServers:
            server.addEndpoint(self)

    def getSavableLatency(self, server, video):
        if server not in self.cacheServers:
            raise "Server not found in this endpoint!"

        if (video in self.videosLatencyMap):
            return max(0, (self.videosLatencyMap[video] - self.cacheServers[server]) * self.videosCountMap[video])
        else:
            return 0

    def addVideo(self, server, video):
        if server not in self.cacheServers:
            raise "Server not found in this endpoint!"

        if (video in self.videosLatencyMap):
            if (self.videosLatencyMap[video] > self.cacheServers[server]):
                for request in self.videosRequestsMap:
                    request.saved += self.videosLatencyMap[video] - self.cacheServers[server]

                self.videosLatencyMap[video] = self.cacheServers[server]


    def getCacheServer(self, index):
        return self.cacheServers[index][1]

    def getCacheServerLatency(self, index):
        return self.cacheServers[index][0]

    def addRequest(self, request):
        self.requests.append(request)

        if request.video not in self.videosRequestsMap:
            self.videosRequestsMap[request.video] = []
            self.videosLatencyMap[request.video] = self.latency
            self.videosCountMap[request.video] = 0

        self.videosCountMap[request.video] += request.count
        self.videosRequestsMap[request.video].append(request)

    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "EP%03s(L: %s, #Ser: %s)" % (self.No, self.latency, len(self.cacheServers))

