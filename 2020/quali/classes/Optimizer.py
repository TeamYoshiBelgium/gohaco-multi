class Optimizer:
    def __init__(self, books, libraries, scanDays):
        self.books = books
        self.libraries = libraries
        self.max = scanDays

        self.T = 0


    def init(self):
        pass

    def preprocess(self):
        pass
        # print(self.orders[1], self.orders[1].orders[:20])

    def optimize(self):
        self.preprocess()



