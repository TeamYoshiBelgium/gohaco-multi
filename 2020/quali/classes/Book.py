class Book:
    CNTR = 0

    def __init__(self, O, id, score):
        self.O = O

        self.id = id
        self.score = score
        self.libraries = []

        self.No = Book.CNTR
        Book.CNTR += 1

        self.done = False
        self.library = None

    def addLibrary(self, Library):
        self.libraries.append(Library)

    def setLibrary(self, Library):
        self.done = True
        self.library = Library

    def get_score(self):
        if (self.done is True):
            raise Exception("Book already done?")

        return self.score / len(self.libraries)


