from tqdm import tqdm
from heapq import *

class Optimizer:
    def __init__(self):
        self.books = []
        self.libraries = []
        self.max = 0

        self.used_libraries = []

        self.T = 0

    def init(self):
        pass

    def preprocess(self):
        for book in tqdm(self.books):
            book.calc_library_scores()
        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):
        # self.preprocess()

        # for book in self.books:
        #     print(book.libraries)
        # exit

        while True:
            bestLibraries = []
            for library in self.libraries:
                if library.done:
                    continue

                score = library.get_score()
                if score > 0:
                    # print((score, library))
                    heappush(bestLibraries, (-score, library))

            for tup in bestLibraries[:1]:
                # print("Adding", tup)
                library = tup[1]

                library.finish()
                library.done = True
                if len(library.scanned_books) > 0:
                    self.used_libraries.append(library)
                    self.T += library.signup

            if len(bestLibraries) == 0:
                break
