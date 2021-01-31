import math


class Library:
    CNTR = 0

    def __init__(self, O, id, books_count, signup, rate, books):
        self.O = O

        self.done = False
        self.books_count = books_count
        self.No = Library.CNTR
        self.rate = rate
        self.signup = signup
        self.books = books

        self.scanned_books = []

        Library.CNTR += 1

    def calc_book_probability(self):
        return sum(map(lambda book: book.counter, self.books))

    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No

    # def __eq__(self, other):
    #     return self.No == other.No

    def __str__(self):
        return "LIB%05d(R:%-3d, S:%-2d, D: %s)" % (self.No, self.rate, self.signup, str(self in self.O.used_libraries)[0])

    def __repr__(self):
        return "LIB%05d(R:%-3d, S:%-2d, D: %s)" % (self.No, self.rate, self.signup, str(self in self.O.used_libraries)[0])

    def __hash__(self):
        return self.No
