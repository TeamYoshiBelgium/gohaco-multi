import math

class Writer:
    def __init__(self, L):
        self.L = L

    def write(self):
        score = 0
        actions = []
        for library in self.L.O.used_libraries:
            for book in library.scanned_books:
                score += book.score

        filename = self.L.filename.replace(".in", "." + str(score) + ".out").replace("in/", "out/")

        with open(filename, 'w+') as file:
            file.write(str(len(self.L.O.used_libraries)))
            file.write("\n")
            for library in self.L.O.used_libraries:
                file.write(str(library.No) + " " + str(len(library.scanned_books)))
                file.write("\n")
                for book in library.scanned_books:
                    file.write(str(book.No) + " ")
                file.write("\n")

        print(self.L.filename, "=>", filename)

        print("SCORE:", score)
