import numpy as np

class Loader:
    def __init__(self, filename): #, heuristic_useless, heuristic_signup, heuristic_bookcount, heuristic_realdays, trim):
        print("Filename:", filename)
        self.books = []
        self.libraries = []
        self.signups = []
        self.rates = []

        self.filename = filename
        with open(filename) as file:
            self.readHeaderLine(file)
            self.readBooks(file)
            self.readLibraries(file)

            # for library in self.libraries:
            #     print(len(library.books))

    def readHeaderLine(self, file):
        row = file.readline().split(" ")

        self.bookCount = int(row[0])
        self.libraryCount = int(row[1])
        self.days = int(row[2])
        pass

    def readBooks(self, file):
        row = file.readline().split(" ")

        book_id = 0
        for book_score_str in row:
            book_id += 1
            book_score = int(book_score_str)
            self.books.append(book_score)

    def readLibraries(self, file):
        self.libraries = []
        id = 0

        for id in range(self.libraryCount):
            row = file.readline()
            splitted = row.split(" ")
            books_count = int(splitted[0])
            signup_time = int(splitted[1])
            books_day = int(splitted[2])

            self.signups.append(signup_time)
            self.rates.append(books_day)

            next_row = file.readline().split(" ")
            book_ids = []
            for book_id in next_row:
                book_ids.append(int(book_id))

            book_ids = set(book_ids)

            books = []

            for i in range(self.bookCount):
                if i in book_ids:
                    books.append(1)
                else:
                    books.append(0)

            self.libraries.append(books)

    def sortBooks(self):
        indexOrder = np.argsort(self.books)[::-1]

        newLibs = []
        for library in self.libraries:
            newLib = np.array(library)[indexOrder]
            newLibs.append(newLib)

        self.libraries=np.array(newLibs).copy()
        self.books=np.array(self.books)[indexOrder].copy()
        self.indexOrder = indexOrder
        self.signups=np.array(self.signups)
        self.rates=np.array(self.rates)
