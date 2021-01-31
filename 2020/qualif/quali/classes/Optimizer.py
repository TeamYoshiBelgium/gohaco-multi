from tqdm import tqdm

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
        self.preprocess()

        # for book in self.books:
        #     print(book.libraries)
        # exit

        orderedBooks = sorted(
            self.books,
            reverse=True,
            key=lambda x: x.calc_score()
        )
        daysleft = self.max


        for book in tqdm(orderedBooks):
            if book.done:
                continue

            bestLibrary = None
            bestScore = 0
            for library in book.libraries:
                if library.done:
                    continue

                score = library.get_score()
                if score > bestScore:
                    bestScore = score
                    bestLibrary = library

            if bestLibrary is not None:
                daysNeeded = bestLibrary.finish()
                self.used_libraries.append(bestLibrary)
                self.T += bestLibrary.signup

                print("Library", bestLibrary, "chosen with score", bestScore)
                daysleft -= daysNeeded





