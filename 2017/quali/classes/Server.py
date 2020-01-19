class Server:
    CNTR = 0

    def __init__(self, Optimizer):
        self.O = Optimizer
        self.No = Server.CNTR

        self.fill = 0
        self.maxSize = self.O.X

        Server.CNTR += 1

        self.endpoints = set()
        self.videos = set()

    def addEndpoint(self, endpoint):
        self.endpoints.add(endpoint)

    def addVideo(self, video):
        self.fill += video.size
        if (self.fill > self.maxSize):
            raise "Overfilled server! " + self + " by adding " + video

        self.videos.add(video)

        for endpoint in self.endpoints:
            endpoint.addVideo(self, video)

    def getScore(self, video):
        if video in self.videos:
            raise "Video already in this server"

        totalScore = 0
        for endpoint in self.endpoints:
            totalScore += endpoint.getSavableLatency(self, video)

        return totalScore


    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "SERV%03s()" % (self.No)

