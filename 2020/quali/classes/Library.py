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

        self.days_needed = math.ceil(self.books_count * 1.0 / self.rate)
        self.book_score = self.get_book_score()
        for book in self.books:
            book.addLibrary(book, self)

        self.scanned_books = []

        # Time at which the library starts signup process
        self.T = -1

        Library.CNTR += 1

    def get_score(self):
        if self.signup + self.O.T > self.O.max:
            return -1

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))

        days = self.O.max - (self.O.T + self.signup)
        filteredBooks = filteredBooks[:days * self.rate]

        sortedBooks = list(sorted(
            map(lambda book: book.score, filteredBooks),
            reverse=True
        ))

        realDays = math.ceil(len(sortedBooks) / self.rate)
        useless = self.O.max - self.O.T - self.signup - realDays

        # TODO investigate average rate?
        score = sum(sortedBooks) * (realDays / (useless + self.signup))
        return score


    def get_book_score(self):
        book_scores = 0
        for book in self.books:
            book_score = book.get_score()
            book_scores += book_score
        return book_scores

    def finish(self):
        self.T = self.O.T

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))

        days = self.O.max - (self.O.T + self.signup)
        filteredBooks = filteredBooks[:days * self.rate]

        sortedBooks = sorted(
            filteredBooks,
            reverse=True,
            key=lambda book: book.score
        )

        for book in sortedBooks:
            book.done = True
            book.library = self

        self.done = True

        self.scanned_books = sortedBooks

        days_needed = self.signup 
        return 0

    def __str__(self):
        return "LIB%s(R:%s, S:%s)" % (self.No, self.rate, self.signup)

    def __repr__(self):
        return "LIB%s(R:%s, S:%s)" % (self.No, self.rate, self.signup)
