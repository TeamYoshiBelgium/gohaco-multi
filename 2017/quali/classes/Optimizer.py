import copy
import random
import sys

from heapq import *
from tqdm import tqdm


class Optimizer:
    def __init__(self, filename,  serverLimit, videoLimit, iterationAddCount):
        self.videos = []
        self.servers = []
        self.endpoints = []
        self.requests = []

        self.filename = filename
        self.serverLimit = serverLimit
        self.videoLimit = videoLimit
        self.iterationAddCount = iterationAddCount

    def init(self, Loader, products, warehouses, orders):
        # self.products = products
        # self.warehouses = warehouses
        # self.orders = orders
        # self.L = Loader
        # self.drones = []

        # for i in range(self.L.drones):
        #     self.drones.append(Drone(self))
        pass

    def optimize(self):
        print("[OPT] Starting optimization", flush=True)

        serverLimit = self.serverLimit
        videoLimit = self.videoLimit
        iterationAddCount = self.iterationAddCount
        fullVideos = False

        totalServerFill = 0
        maxFill = len(self.servers) * self.servers[0].maxSize

        videos = copy.copy(self.videos)

        while True:
            heap = []
            remove = []

            if fullVideos is False:
                for video in videos[:videoLimit]:
                    (score, server) = video.findBestServer(serverLimit)

                    if (server is not None):
                        heappush(heap, (-score/video.size, server, video))
                    else:
                        remove.append(video)

                if len(heap) == 0:
                    iterationAddCount = max(int(iterationAddCount / 2), 1)
                    fullVideos = False

            if fullVideos is True:
                for video in videos:
                    (score, server) = video.findBestServer(serverLimit)

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
                    video.addServer(server)
                    print(score, video, server, flush=True)
                    added += 1
                    totalServerFill += video.size
                except:
                    print("FAIL", score, video, server, flush=True)
                    # print(sys.exc_info())
                    # exit()
                    pass
            print(self.filename)
            print("Added %d/%d heap(%d)" % (added, max(1,min(int(L/10), iterationAddCount)), L))
            print("Total fill: %d/%d   (%.2f%%)" % (totalServerFill, maxFill, totalServerFill/maxFill*100))
            print("=================================", flush=True)

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
