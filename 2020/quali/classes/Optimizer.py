class Optimizer:
    def __init__(self):
        self.books = []
        self.libraries = []
        self.max = []

        self.T = 0

    def init(self):
        pass

    def preprocess(self):
        pass
        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):
        self.preprocess()

        orderedBooks = sorted(
            self.books,
            reverse=True,
            key=lambda x: x.get_score()
        )

        for book in orderedBooks:
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

            if library is not None:
                library.finish()
                self.T += library.signup
                print("Library", library, "chosen")





