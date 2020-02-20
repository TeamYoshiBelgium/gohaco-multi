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

    def calc_score(self):
        if (self.done is True):
            raise Exception("Book already done?")

        return self.score / len(self.libraries)


    def __str__(self):
        return 'Book (%i %i %s)' % (self.id, self.score, self.done)

    def __repr__(self):
        return str(self)
    