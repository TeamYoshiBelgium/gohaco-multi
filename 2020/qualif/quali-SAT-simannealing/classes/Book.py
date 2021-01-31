from heapq import *


class Book:
    CNTR = 0

    def __init__(self, O, id, score):
        self.O = O

        self.No = Book.CNTR
        Book.CNTR += 1
        self.score = score
        self.libraries = []
        self.inLibraries = []
        self.done = False
        self.counter = 0

    def addLibrary(self, Library):
        self.libraries.append(Library)

    def setLibrary(self, Library):
        self.done = True
        self.library = Library

    def __str__(self):
        return 'B%i(%i %s %d)' % (self.No, self.score, str(self.done)[0], self.counter)

    def __repr__(self):
        return str(self)


    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No

    def __hash__(self):
        return self.No
