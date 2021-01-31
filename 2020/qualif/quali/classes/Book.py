from heapq import *


class Book:
    CNTR = 0

    def __init__(self, O, id, score):
        self.O = O

        self.id = id
        self.score = score
        self.libraries = []

        self.No = Book.CNTR
        Book.CNTR += 1

        self.done = False
        self.library = None

        self.sortedLibraries = []

        self.scores = {}
        self.used = None

    def addLibrary(self, Library):
        self.libraries.append(Library)

    def setLibrary(self, Library):
        self.done = True
        self.library = Library

    def init_libraries(self):
        self.available = []
        for library in self.O.used_libraries:
            if library in self.libraries:
                self.available.append(library)

    def find_best_library(self):
        original = self.used
        beat = 0
        if (self.used is not None):
            original.booksPrioQueue.remove((self.score, self))
            self.used = None
            bestReplacement = None
            bestScore = 0
            for book in original.books:
                if book.used is not None:
                    continue

                if book == self:
                    continue

                if (book.score, book) in original.booksPrioQueue:
                    continue

                if book.score > bestScore:
                    bestScore = book.score
                    bestReplacement = book

            if bestReplacement is not None:
                heappush(original.booksPrioQueue, (bestReplacement.score, bestReplacement))
                bestReplacement.used = original
            else:
                self.used = original
                heappush(original.booksPrioQueue, (self.score, self))
                return None

        best = None
        bestScore = 0
        bestLen = 99999
        pop = True
        for library in self.available:
            if len(library.booksPrioQueue) < library.calc_capacity():
                best = library
                bestScore = 1
                pop = False
                break
            else:
                # Even the last element is bigger
                first = library.booksPrioQueue[0][0]
                if (first > self.score):
                    continue
                else:
                    score = self.score - first
                    if (score > bestScore):
                        best = library
                        bestScore = score
                        bestLen = len(library.booksPrioQueue)
                    elif (score == bestScore and len(library.booksPrioQueue) > bestLen):
                        best = library
                        bestScore = score
                        bestLen = len(library.booksPrioQueue)

        if best is None:
            return None

        if pop:
            replaced = heappushpop(best.booksPrioQueue, (self.score, self))
            replaced[1].used = None
        else:
            heappush(best.booksPrioQueue, (self.score, self))
        self.used = best

        if best == original:
            return None

        return best



    def calc_library_scores(self):
        libraries = []

        for library in self.libraries:
            score = library.get_score()
            libraries.append(
                (score, library)
            )

        libraries = list(sorted(
            libraries,
            reverse=True,
            key=lambda tup: tup[0]
        ))

        self.sortedLibraries = libraries

    def calc_score(self):
        if len(self.libraries) == 0:
            return -1

        bestScore = 0
        for tup in self.sortedLibraries:
            if tup[1].done:
                continue
            else:
                bestScore = tup[0]
                break

        return self.score * bestScore

    def withlibrary_score(self):
        if self.O.heuristic_bookcount == 0:
            return self.score

        return self.score - len(self.libraries) / self.O.heuristic_bookcount


    def __str__(self):
        return 'B%i(%i %s)' % (self.id, self.score, str(self.done)[0])

    def __repr__(self):
        return str(self)


    def __gt__(self, other):
        return self.No > other.No

    def __lt__(self, other):
        return self.No > other.No
