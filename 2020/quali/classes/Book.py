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

        self.sortedLibraries = []

    def addLibrary(self, Library):
        self.libraries.append(Library)

    def setLibrary(self, Library):
        self.done = True
        self.library = Library

    def calc_library_scores(self):
        libraries = []

        for library in self.libraries:
            score = library.get_score()
            libraries.append(
                (score, library)
            )

        libraries = list(sorted(
            libraries,
            reverse=True,
            key=lambda tup: tup[0]
        ))

        self.sortedLibraries = libraries

    def calc_score(self):
        if len(self.libraries) == 0:
            return -1

        bestScore = 0
        for tup in self.sortedLibraries:
            if tup[1].done:
                continue
            else:
                bestScore = tup[0]
                break

        return self.score * bestScore


    def __str__(self):
        return 'Book%i(%i %s)' % (self.id, self.score, self.done)

    def __repr__(self):
        return str(self)
