class Optimizer:
    def __init__(self):
        self.books = []
        self.libraries = []
        self.max = []

        self.used_libraries = []

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
<<<<<<< HEAD
            key=lambda x: x.calc_score()
=======
            key=lambda x: x.get_score()
>>>>>>> 8af7b303872b49f937556031673a37707494f01a
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
                self.used_libraries.append(library)
                self.T += library.signup
                print("Library", library, "chosen")





