class Book:
    CNTR = 0

    def __init__(self, O, score):
        self.O = O

        self.score = score
        self.libraries = []

        self.No = Book.CNTR
        Book.CNTR += 1

    def addLibrary(self, Library):
        self.libraries.append(Library)

