import math

class Writer:
    def __init__(self, solution, SIGNUP, RATE, TURNS, BOOK_SCORES, filename):
        self.solution = solution
        self.SIGNUP = SIGNUP
        self.RATE = RATE
        self.TURNS = TURNS
        self.BOOK_SCORES = BOOK_SCORES
        self.filename = filename

    def write(self):
        score = 0
        actions = []

        solution_books = self.solution.calculateLibraryBooksMatrix()
        turn = 0
        score = 0
        books = set([])
        for library in solution_books:
            turn += self.SIGNUP[library]
            if turn > self.TURNS:
                print("Turns superceded!!! Max=%d, new=%d" % (self.TURNS, turn))
            maxBooks = (self.TURNS - turn) * self.RATE[library]
            if len(solution_books[library]) > maxBooks:
                print("Max books superceded!!! library: %d, signup: %d, rate: %d, maxTurns: %d, turn: %d, books: %d, maxbooks: %d" % (library, self.SIGNUP[library], self.RATE[library], self.TURNS, turn, len(solution_books[library]), maxBooks))
                # print("Max books superceded!!! Library=%d, Max=%d, Present=%d" % (library, maxBooks, len(solution_books[library])))

            for book in solution_books[library]:
                if book not in books:
                    score += self.BOOK_SCORES[book]
                    books.add(book)

        print("SCORE:", score)

        filename = self.filename.replace(".in", "." + str(score) + ".out").replace("in/", "out/")
        with open(filename, 'w+') as file:
            file.write(str(len(solution_books)))
            file.write("\n")
            for library in solution_books:
                file.write(str(library) + " " + str(len(solution_books[library])))
                file.write("\n")
                for book in solution_books[library]:
                    file.write(str(book) + " ")
                file.write("\n")

        # print(self.L.filename, "=>", filename)

        # print("SCORE:", score)
