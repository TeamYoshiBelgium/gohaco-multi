from .Optimizer import Optimizer


class Loader:
    def __init__(self, filename):
        self.filename = filename
        with open(filename) as file:
            self.O = Optimizer()

            self.readHeaderLine(file)
            self.readBooks(file)
            self.readLibraries(file)

            self.O.optimize()

    def readHeaderLine(self, file):
        row = file.readline().split(" ")

        self.books   = int(row[0])
        self.librariees   = int(row[1])
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
        for row in file.readline():
            splitted = row.split(" ")
            books_count = int(splitted[0])
            signup_time = int(splitted[1])
            books_day = int(splitted[2])

            next_row = file.readline().split(" ")
            books = []
            for book in next_row:
                books.append(int(book))
            id += 1

            library = Library(books_count, signup_time, books_day, books)
            self.libraries.append(library)


