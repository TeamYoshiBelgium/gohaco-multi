class Writer:
    def __init__(self, L, O):
        self.L = L
        self.O = O

    def write(self):
        score = 0
        # actions = []
        # for library in self.L.O.used_libraries:
        #     for book in library.scanned_books:
        #         score += book.score
        #
        # filename = self.L.filename.replace(".in", "." + str(score) + ".out").replace("in/", "out/")
        # filename = filename.replace(".out", ".NEW.out")
        # filename = filename.replace(".out",
        #     "." +
        #     str(self.L.O.heuristic_signup) + "-" +
        #     str(self.L.O.heuristic_wasted) + ".out"
        # )
        #
        # # filename = filename.replace(".out",
        # #     "." +
        # #     str(self.L.O.heuristic_useless) + "-" +
        # #     str(self.L.O.heuristic_signup) + "-" +
        # #     str(self.L.O.heuristic_bookcount) + "-" +
        # #     str(self.L.O.heuristic_realdays) + "-" +
        # #     str(self.L.O.trim) + ".out"
        # # )
        #
        # with open(filename, 'w+') as file:
        #     file.write(str(len(self.L.O.used_libraries)))
        #     file.write("\n")
        #     for library in self.L.O.used_libraries:
        #         file.write(str(library.No) + " " + str(len(library.scanned_books)))
        #         file.write("\n")
        #         for book in library.scanned_books:
        #             file.write(str(book.No) + " ")
        #         file.write("\n")
