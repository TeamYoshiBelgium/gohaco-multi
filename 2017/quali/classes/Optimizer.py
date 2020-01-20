import copy
import random
import sys
import datetime

from heapq import *
from tqdm import tqdm


class Optimizer:
    def __init__(self, filename,  videoLimit, iterationAddCount):
        self.videos = []
        self.servers = []
        self.endpoints = []
        self.requests = []

        self.filename = filename
        self.videoLimit = videoLimit
        self.iterationAddCount = iterationAddCount

    def init(self):
        # self.products = products
        # self.warehouses = warehouses
        # self.orders = orders
        # self.L = Loader
        # self.drones = []

        # for i in range(self.L.drones):
        #     self.drones.append(Drone(self))

        for request in self.requests:
            request.video.endpoints.add(request.endpoint)

        for video in self.videos:
            for endpoint in video.endpoints:
                for server in endpoint.cacheServers:
                    video.servers.add(server)

        for video in tqdm(self.videos):
            video.calcBestServers()

    def optimize(self):
        self.init()
        print("[OPT] Starting optimization", flush=True)

        videoLimit = self.videoLimit
        iterationAddCount = self.iterationAddCount
        print(videoLimit, iterationAddCount)
        fullVideos = False

        totalServerFill = 0
        maxFill = len(self.servers) * self.servers[0].maxSize

        videos = copy.copy(self.videos)

        it = 0

        while True:
            heap = []
            remove = []

            if fullVideos is False:
                for video in videos[:videoLimit]:
                    (score, server) = video.findBestServer()

                    if (server is not None):
                        heappush(heap, (-score/video.size, server, video))
                    else:
                        remove.append(video)

                if len(heap) == 0:
                    iterationAddCount = max(int(iterationAddCount / 2), 1)
                    fullVideos = False

            if fullVideos is True:
                for video in videos:
                    (score, server) = video.findBestServer()

                    if (server is not None):
                        heappush(heap, (-score/video.size, server, video))
                    else:
                        remove.append(video)

            if len(heap) == 0:
                break

            added=0
            L = len(heap)
            for x in heap[:max(1,min(int(L/10), iterationAddCount))]:
                (score, server, video) = heappop(heap)
                try:
                    server.addVideo(video)
                    # print(score, video, server, flush=True)
                    added += 1
                    totalServerFill += video.size
                except:
                    # print("FAIL", score, video, server, flush=True)
                    # print(sys.exc_info())
                    # exit()
                    pass

            if (it % 100 == 0):
                print(datetime.datetime.now().strftime('%H:%M:%S'), self.filename, end=" ")
                print("Total fill: %d/%d   (%.2f%%)" % (totalServerFill, maxFill, totalServerFill/maxFill*100))
            it += 1

            # for video in remove:
            #     videos.remove(video)

            random.shuffle(videos)


            # keep = copy.copy(videos)
            # bestVideo = None
            # bestServer = None
            # bestScore = 0

            # random.shuffle(keep)

            # for video in keep[:limit]:
            #     (score, server) = video.findBestServer(100)

            #     if server is None:
            #         (score, server) = video.findBestServer(len(self.servers))

            #     if server is None:
            #         videos.remove(video)
            #         continue

            #     if ((score/video.size) > bestScore):
            #         bestVideo = video
            #         bestServer = server
            #         bestScore = (score/video.size)

            # if bestServer is None:

            #     if limit == len(self.videos):
            #         break

            #     limit = len(self.videos)

            # else:
            #     bestServer.addVideo(bestVideo)
            #     bestVideo.addServer(server)

            # print("", flush=True)
            # print("", flush=True)

        print("[OPT] Finished")
