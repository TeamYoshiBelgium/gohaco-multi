import copy
import random

from heapq import *
from tqdm import tqdm


class Optimizer:
    def __init__(self):
        self.videos = []
        self.servers = []
        self.endpoints = []
        self.requests = []

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

        limit = 200
        videos = copy.copy(self.videos)

        while True:
            heap = []
            keep = []

            for video in tqdm(videos):
                (score, server) = video.findBestServer(len(self.servers))

                if (server is not None):
                    heappush(heap, (-score/video.size, server, video))
                    keep.append(video)

            if len(heap) == 0:
                break

            for i in range(len(heap)):
                (score, server, video) = heappop(heap)

                try:
                    server.addVideo(video)
                    video.addServer(server)
                    print(score, video, server)
                except:
                    pass

            print("=================================")

            videos = keep


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
