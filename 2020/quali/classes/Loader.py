from .Optimizer import Optimizer
from .Library import Library
from .Book import Book


class Loader:
    def __init__(self, filename):
        self.books = []
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer()

            self.readHeaderLine(file)
            self.readBooks(file)
            self.readLibraries(file)

            for library in self.libraries:
                print(len(library.books))

            self.O.books = self.books
            self.O.libraries = self.libraries
            self.O.days = self.days
            self.O.optimize()

    def readHeaderLine(self, file):
        row = file.readline().split(" ")

        self.books_length = int(row[0])
        self.librariees = int(row[1])
        self.days = int(row[2])
        pass

    def readBooks(self, file):
        row = file.readline().split(" ")
        self.book_scores = []
        book_id = 0
        for book_score_str in row:
            book_id += 1
            book_score = int(book_score_str)
            self.book_scores.append(book_score)
            book = Book(self.O, book_id, book_score)
            self.books.append(book)

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
            library = Library(self.O, id, books_count, signup_time, books_day, books)
            for book_id in next_row:
                book = self.books[int(book_id)]
                books.append(book)
                book.addLibrary(library)
            id += 1

            self.libraries.append(library)
