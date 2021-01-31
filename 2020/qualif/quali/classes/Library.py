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

        self.minScanScore = 0
        self.scanned_books = []
        self.wastedTime = 0

        self.virtualBooks = []
        self.virtualDone = False

        self.booksPrioQueue = []

        # Time at which the library starts signup process
        self.T = -1

        Library.CNTR += 1

    # def book_score(self, book):
    #     return book.score - len()

    def get_score(self):
        if self.signup + self.O.T >= self.O.max:
            return -1

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))

        sortedBooks = list(sorted(
            map(lambda book: book.withlibrary_score(), filteredBooks),
            reverse=True
        ))

        days = self.O.max - (self.O.T + self.signup)
        sortedBooks = sortedBooks[:days * self.rate]

        realDays = math.ceil(len(sortedBooks) / self.rate)
        useless = min(0, self.O.max - self.O.T - self.signup - realDays)

        # TODO investigate average rate?
        score = sum(sortedBooks)*(realDays**self.O.heuristic_realdays) / (
            useless**self.O.heuristic_useless * self.O.heuristic_useless +
            self.signup**self.O.heuristic_signup
        )
        return score

    def raw_score(self, T):
        if self.signup + T >= self.O.max:
            return -1

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))

        sortedBooks = list(sorted(
            map(lambda book: book.withlibrary_score(), filteredBooks),
            reverse=True
        ))

        days = self.O.max - (T + self.signup)
        sortedBooks = sortedBooks[:days * self.rate]

        score = sum(sortedBooks)

        return score


    def get_book_score(self):
        book_scores = 0
        for book in self.books:
            book_score = book.get_score()
            book_scores += book_score
        return book_scores

    def finish2(self):
        self.T = self.O.T
        self.scanned_books = self.virtualBooks[:(self.O.max - self.O.T - self.signup) * self.rate]

        for book in self.scanned_books:
            book.done = True

        for library in self.O.libraries:
            if library.done:
                continue

            for book in self.scanned_books:
                if book in library.virtualBooks:
                    library.virtualBooks.remove(book)

        self.done = True

    def calc_capacity(self):
        return (self.O.max - self.T - self.signup) * self.rate

    def calc_virtual_score(self):
        count = max(0,(self.O.max - self.O.T - self.signup) * self.rate)
        if (count == 0):
            return 0

        relevantBooks = self.virtualBooks[:count]
        score  = sum(map(lambda book: book.score, relevantBooks))
        score /= (self.signup**self.O.heuristic_signup)

        if (self.virtualDone) and self.O.heuristic_wasted != 0:
            score *= self.O.heuristic_wasted
            score *= len(relevantBooks)/((self.max - self.T - self.signup)*self.rate)

        return score

    def finish(self):
        if (self.O.T + self.signup > self.O.max):
            return

        self.T = self.O.T

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))

        sortedBooks = sorted(
            filteredBooks,
            reverse=True,
            key=lambda book: book.withlibrary_score()
        )

        days = self.O.max - (self.O.T + self.signup)
        sortedBooks = sortedBooks[:days * self.rate]

        for book in sortedBooks:
            book.done = True
            book.library = self

        self.done = True

        self.scanned_books = sortedBooks

        self.wastedTime = self.O.max - (self.O.T + math.ceil(len(sortedBooks)/self.rate))

        if (len(sortedBooks) > 0):
            self.minScanScore = min(map(
                lambda book: book.score,
                sortedBooks
            ))

    def finish_with_later(self, librariesWithIgnorableBooks):
        self.T = self.O.T

        filteredBooks = list(filter(
            lambda book: not book.done,
            self.books
        ))


        # newfiltered = list(filteredBooks)
        # # print(len(list(filteredBooks)), end=" ")

        # for library in librariesWithIgnorableBooks:

        #     newfiltered = list(filter(
        #         lambda book: book in library.books and book.score > library.minScanScore,
        #         newfiltered
        #     ))

        sortedBooks = sorted(
            filteredBooks,
            reverse=True,
            key=lambda book: book.withlibrary_score()
        )
        # sortedFilteredBooks = sorted(
        #     newfiltered,
        #     reverse=True,
        #     key=lambda book: book.withlibrary_score()
        # )

        days = self.O.max - (self.O.T + self.signup)

        sortedBooks = sortedBooks[:days * self.rate]
        # sortedFilteredBooks = sortedFilteredBooks[:days * self.rate]

        # if (len(sortedFilteredBooks) < days * self.rate):
        #     for book in sortedBooks:
        #         if book not in sortedFilteredBooks:
        #             sortedFilteredBooks.append(book)

        for book in sortedBooks:
            book.done = True
            book.library = self

        self.done = True
        # print(len(sortedBooks), len(sortedBooks))
        self.scanned_books = sortedBooks
        # if (len(sortedBooks) != len(sortedBooks)):
        #     print(self)

    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No

    def __str__(self):
        return "LIB%03d(R:%-3d, S:%-2d, D: %s)" % (self.No, self.rate, self.signup, str(self in self.O.used_libraries)[0])

    def __repr__(self):
        return "LIB%03d(R:%-3d, S:%-2d, D: %s)" % (self.No, self.rate, self.signup, str(self in self.O.used_libraries)[0])
