from .Optimizer import Optimizer
from .Library import Library
from .Book import Book


class Loader:
    def __init__(self, filename):
        self.books = []
        self.filename = filename
        with open(filename) as file:
            self.O = 1
            # self.O = Optimizer()

            self.readHeaderLine(file)
            self.readBooks(file)
            self.readLibraries(file)

            for library in self.libraries:
                print(len(library.books))

    #            self.O.optimize()

    def readHeaderLine(self, file):
        row = file.readline().split(" ")

        self.books_length = int(row[0])
        self.librariees = int(row[1])
        self.days = int(row[2])
        pass

    def readBooks(self, file):
        row = file.readline().split(" ")
        self.book_scores = []
        for book in row:
            self.book_scores.append(int(book))

        pass

    def readLibraries(self, file):
        self.libraries = []
        id = 0

        for id in range(self.librariees):
            row = file.readline()
            splitted = row.split(" ")
            books_count = int(splitted[0])
            signup_time = int(splitted[1])
            books_day = int(splitted[2])

            next_row = file.readline().split(" ")
            books = []
            library = Library(self.O, books_count, signup_time, books_day, books)
            for book_id in next_row:
                book = Book(self.O, book_id, self.book_scores[int(book_id)])
                books.append(book)
            id += 1

            self.libraries.append(library)
