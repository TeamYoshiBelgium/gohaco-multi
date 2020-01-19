
from .Video import Video
from .Server import Server
from .Endpoint import Endpoint
from .Request import Request

# from .Warehouse import Warehouse
# from .Order import Order
from .Optimizer import Optimizer


class Loader:
    def __init__(self, filename, serverLimit, videoLimit, iterationAddCount):
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer(filename, serverLimit, videoLimit, iterationAddCount)
            self.file = file

            self.readHeaderLine()

            self.videos = []
            self.readVideoSizes()

            self.servers = []
            for i in range(self.C):
                self.servers.append(Server(self.O))

            self.endpoints = []
            self.readEndpoints()

            self.requests = []
            self.readRequests()

            self.O.videos = self.videos
            self.O.servers = self.servers
            self.O.endpoints = self.endpoints
            self.O.requests = self.requests

            print( "FILE:        " , filename)
            print( "Videos:      " , len(self.videos))
            print( "Servers:     " , len(self.servers))
            print( "Endpoints:   " , len(self.endpoints))
            print( "Requests:    " , len(self.requests))
            print( "Server cap.: " , self.X)
#

    def readHeaderLine(self):
        row = self.file.readline().split(" ")

        self.V   = int(row[0])
        self.O.V = int(row[0])

        self.E   = int(row[1])
        self.O.E = int(row[1])

        self.R   = int(row[2])
        self.O.R = int(row[2])

        self.C   = int(row[3])
        self.O.C = int(row[3])

        self.X   = int(row[4])
        self.O.X = int(row[4])

    def readVideoSizes(self):
        row = [ int(x) for x in self.file.readline().split(" ") ]

        if len(row) != self.V:
            raise "vidcount problem"

        for i in range(self.V):
            self.videos.append(Video(self.O, row[i]))

    def readEndpoints(self):
        for i in range(self.E):
            row = [ int(x) for x in self.file.readline().split(" ") ]
            dataLat, conServCnt = row[0], row[1]

            connectedServers = {}
            for i in range(conServCnt):
                row2 = [ int(x) for x in self.file.readline().split(" ") ]
                connectedServers[self.servers[row2[0]]] = row2[1]

            self.endpoints.append(Endpoint(self.O, dataLat, connectedServers))

    def readRequests(self):
        for i in range(self.R):
            row = [ int(x) for x in self.file.readline().split(" ") ]

            video = self.videos[row[0]]
            endpoint = self.endpoints[row[1]]
            count = row[2]
            self.requests.append(Request(self.O, video, endpoint, count))
