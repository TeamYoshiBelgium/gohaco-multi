import random
import bisect
import collections
import time
import numpy as np
from multiprocessing import Pool
from classes.Loader import Loader
from classes.Writer import Writer

SIGNUP = None
RATES = None
SCORES = None
LIBRARY_BOOKS = None
TURNS = None

LIBRARIES = []
SORTED_LIBRARY_INDEXES = []
SORTED_LIBRARY_SIGNUPS = []



class Solution():
    def __init__(self, library_indexes):
        self.library_indexes = library_indexes

        if len(library_indexes) > 0:
            self._library_max_books_scannable = np.multiply(TURNS-np.cumsum(SIGNUP[library_indexes]), RATES[library_indexes])
            self._margin = TURNS-np.sum(SIGNUP[library_indexes])
            if (self._margin < 0):
                raise "Wut, our sum is bigger than allowed turns!"
        else:
            self._library_max_books_scannable = np.zeros(len(SIGNUP))
            self._margin = TURNS

        self._score = None
        self._hash = None

    def calcScore(self):
        if (self._score != None):
            return self._score
        if len(self.library_indexes) == 0:
            return 0

        books = set([])
        start = time.time()

        # Small optimization: we sort libraries by available book count
        library_indexes = self.library_indexes[np.argsort(self._library_max_books_scannable)]
        original_indexes = np.argsort(self._library_max_books_scannable)

        # While there are still scannable books in our solution set,
        # loop over our libraries (sorted by book count asc), and fill them with a book
        # if the library is exhausted, make sure it's scannable book
        rng = range(len(library_indexes))
        removed = set([])
        while np.sum(self._library_max_books_scannable) > 0:
            removed.clear()
            added = False
            for i_index in rng:
                i_library = library_indexes[i_index]
                i_original_index = original_indexes[i_index]

                if self._library_max_books_scannable[i_original_index] == 0:
                    continue

                best_book = LIBRARIES[i_library].findBestBookIndex(books)
                if best_book is None:
                    self._library_max_books_scannable[i_original_index] = 0
                    removed.add(i_index)
                else:
                    # print("Found book: %d, library: %d" % (best_book, i_library), flush=True)
                    if best_book in books:
                        raise "Wut? book %s already found!" % best_book
                    self._library_max_books_scannable[i_original_index] -= 1
                    books.add(best_book)
                    added = True

            if added is False:
                break

            if len(removed) > 0:
                rng = [ item for item in rng if item not in removed ]

        books = np.fromiter(books, int, len(books))
        self._score = np.sum(SCORES[books])
        return self._score

    def calculateLibraryBooksMatrix(self):
        if len(self.library_indexes) == 0:
            return np.array([[]])

        self._library_max_books_scannable = np.multiply(TURNS-np.cumsum(SIGNUP[self.library_indexes]), RATES[self.library_indexes])

        books = set([])
        start = time.time()

        # Small optimization: we sort libraries by available book count
        library_indexes = self.library_indexes[np.argsort(self._library_max_books_scannable)]
        original_indexes = np.argsort(self._library_max_books_scannable)
        libraries_book_matrix = collections.OrderedDict()
        for library in self.library_indexes:
            libraries_book_matrix[library] = []


        # While there are still scannable books in our solution set,
        # loop over our libraries (sorted by book count asc), and fill them with a book
        # if the library is exhausted, make sure it's scannable book
        while np.sum(self._library_max_books_scannable) > 0:
            added = False
            for i_index in range(len(library_indexes)):
                i_library = library_indexes[i_index]
                i_original_index = original_indexes[i_index]

                if self._library_max_books_scannable[i_original_index] == 0:
                    continue

                best_book = LIBRARIES[i_library].findBestBookIndex(books)
                if best_book is None:
                    self._library_max_books_scannable[i_original_index] = 0
                else:
                    # print("Found book: %d, library: %d" % (best_book, i_library), flush=True)
                    if best_book in books:
                        raise "Wut? book %s already found!" % best_book
                    self._library_max_books_scannable[i_original_index] -= 1
                    books.add(best_book)

                    libraries_book_matrix[i_library].append(best_book)

                    added = True

            if added is False:
                break

        return libraries_book_matrix

    '''
        Tries to find a neighbour aolution by randomly switching the order of two elements in the libraries list
    '''
    def find_switch_neighbour(self):
        if len(self.library_indexes) < 2:
            return None

        L = len(self.library_indexes)
        r1 = random.randint(0, L-1)
        r2 = random.randint(0, L-1)
        while r1 == r2:
            r2 = random.randint(0, L-1)

        newLibraries = np.copy(self.library_indexes)
        newLibraries[r1], newLibraries[r2] = newLibraries[r2], newLibraries[r1]

        return Solution(newLibraries)


    '''
        Tries to find a neighbour solution by removing a random library and adding
        a new random library that is not yet present, while maintining
        sum(libraries) < TURNS.
        If after removing one library no replacement can be found,
        we keep removing libraries until we find enough room for a replacement.
    '''
    def find_swap_neighbour(self):
        if len(self.library_indexes) < 2:
            return None

        candidate = None
        signup_turn_bound = self._margin
        newLibraries = np.copy(self.library_indexes)
        removed = set([])
        first_index = None

        while True:
            random_index = random.randrange(len(newLibraries))
            if first_index is None:
                first_index = random_index
            removed_library = newLibraries[random_index]
            newLibraries = np.delete(newLibraries, random_index)
            signup_turn_bound += SIGNUP[removed_library]
            removed.add(removed_library)

            # Retrieve the upper bound for our search space,
            # we will use this to partition the SORTED_LIBRARY_INDEXES array
            # and find a replacement in all relevant candidates
            sorted_library_index_bound = bisect.bisect_left(SORTED_LIBRARY_SIGNUPS, signup_turn_bound+1)
            # print(signup_turn_bound+1)
            # print(SORTED_LIBRARY_SIGNUPS)
            # print(SORTED_LIBRARY_SIGNUPS)
            # if sorted_library_index_bound == 0:
            #     continue

            if sorted_library_index_bound != 0:
                # We do a random roll of our range, such that we get randomized candidates
                for sorted_library_index in np.roll(range(sorted_library_index_bound), random.randrange(sorted_library_index_bound)):
                    library_index = SORTED_LIBRARY_INDEXES[sorted_library_index]
                    if library_index not in removed and library_index not in newLibraries:
                        candidate = library_index
                        break

            if candidate is not None:
                break

            # print(len(newLibraries))
            if len(newLibraries) == 0:
                break

        if candidate is None:
            return None
        else:
            if first_index > len(newLibraries):
                newLibraries = np.append(newLibraries, candidate)
            else:
                newLibraries = np.insert(newLibraries, first_index, candidate)
            return Solution(np.fromiter(newLibraries, int, len(newLibraries)))

    def find_add_neighbour(self):
        sorted_library_index_bound = bisect.bisect_left(SORTED_LIBRARY_SIGNUPS, self._margin+1)
        if sorted_library_index_bound == 0:
            return None
        elif len(self.library_indexes) == 0:
            return Solution(np.array([random.choice(SORTED_LIBRARY_INDEXES)]))
        else:
            candidate = None
            for sorted_library_index in np.roll(range(sorted_library_index_bound), random.randrange(sorted_library_index_bound)):
                library_index = SORTED_LIBRARY_INDEXES[sorted_library_index]
                if library_index not in self.library_indexes:
                    candidate = library_index
                    break

            if candidate is None:
                return None
            else:
                newLibraries = np.copy(self.library_indexes)
                newLibraries = np.append(newLibraries, candidate)
                return Solution(newLibraries)

    def __eq__(self, other):
        if other is None:
            return False
        return hash(self) == hash(other)

    def __hash__(self):
        if self._hash is not None:
            return self._hash

        hashCode = 1
        for el in self.library_indexes:
            hashCode = hashCode * 31 + el
        self._hash = int(hashCode)

        return self._hash

class Library():
    # Library(4,1,np.array([120, 0, 0, 12, 0, 14]))
    '''
        signup = time for library to start scanning
        scanRate = books / day library can scan
        book_scores = list of ALL books, with the potential score of the book:
                        if a book is not in the library, the score is thus
                        rendered as 0
    '''
    def __init__(self, signup, scanRate, book_scores):
        self.signup = signup
        self.scanRate = scanRate

        # We sort the books by score, but want their indexes to be stored
        # np.argsort                            -> sorts book scores ascending
        # [::-1]                                -> revert this, we want descending
        # [:len(book_scores[book_scores != 0])] -> trim away all unavailable books (score=0)
        self.sorted_book_indexes = np.argsort(book_scores)[::-1][:len(book_scores[book_scores != 0])]

        # print(book_scores)
        # print(self.sorted_book_indexes)
        # print(book_scores[self.sorted_book_indexes])


    '''
        Method that returns the best available book for this library,
        ignoring books that are present in `alreadyUsed`
    '''
    def findBestBookIndex(self, alreadyUsedIndexes):
        for book in self.sorted_book_indexes:
            if book not in alreadyUsedIndexes:
                return book

def calcParallelScore(solution):
    start = time.time()
    score = solution.calcScore()
    # print(score)
    return score

def tabuSearch(init, neighboursPerIteration, neighbourFunctions, neighbourFunctionProbabilities, maxIterations=1000, maxDryIterations=50):
    def findProbabilityWeightedRandomIndex(neighbourFunctionProbabilities):
        rnd = random.random()
        i = 0
        carry = neighbourFunctionProbabilities[0]
        while carry < rnd and i < (len(neighbourFunctionProbabilities)-1):
            i += 1
            carry += neighbourFunctionProbabilities[i]

        return i

    def findNeighbours(state, neighboursPerIteration, neighbourFunctions, neighbourFunctionProbabilities, tabu, multiTurnDist=[0.5,0.25,0.25], turn=0):
        neighbours = set([])
        i = 0
        lastIteration = set([state])
        fullArr = []
        for depth in range(len(multiTurnDist)):
            carry = set([])
            while len(carry) < neighboursPerIteration * multiTurnDist[depth]:
                if len(lastIteration) == 0:
                    break

                func_index = findProbabilityWeightedRandomIndex(neighbourFunctionProbabilities)
                neighbour = neighbourFunctions[func_index](random.choice(tuple(lastIteration)))
                if neighbour is not None:
                    if neighbour not in tabu and neighbour not in neighbours and neighbour not in carry:
                        carry.add(neighbour)
                        fullArr.append(depth)
                i += 1
                if i > neighboursPerIteration*500:
                    print("WARN: Neighbour detection reached infinite state it seems... " +
                          "Is your neighboursPerIteration > possible state count or the state space " +
                          "getting exhausted?")

                    break
            lastIteration = carry
            neighbours.update(carry)

        return list(neighbours)

    def elapsed(start):
        return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))

    if len(neighbourFunctions) == 0:
        raise "Need at least 1 neighbour function"

    if len(neighbourFunctions) != len(neighbourFunctionProbabilities):
        raise "Neighbour function probabilities do not match neigbour functions"

    if abs(1.0 - sum(neighbourFunctionProbabilities)) > 0.0000001:
        raise "Neighbour probabilities do not match 1"

    bestCandidate = init
    bestCandidateScore = init.calcScore()

    optimum = init
    optimumScore = init.calcScore()

    tabu = set([init])

    iteration = 0
    dry = 0
    start = time.time()
    print("[%s] TABU START" % elapsed(start))
    with Pool(THREADS) as p:
        while True:
            neighbours = findNeighbours(bestCandidate, neighboursPerIteration, neighbourFunctions, neighbourFunctionProbabilities, tabu, [0.5, 0.25, 0.25])
            if (len(neighbours) == 0):
                print("[%s] NO neighbours found, state space is ~ exhausted" % elapsed(start))
                break

            # neighbours = [ neighbour.find_swap_neighbour() for neighbour in range(10) ]

            scores = p.map(calcParallelScore, neighbours)
            # print(scores)
            bestIndex = np.argmax(scores)
            newBestCandidateScore = scores[bestIndex]
            iteration += 1

            print("[%s] ITERATION %d, optimum=%d, previous=%d, new=%d, dry=%d" % (elapsed(start), iteration, optimumScore, bestCandidateScore, newBestCandidateScore, dry))

            dry += 1
            if newBestCandidateScore > optimumScore:
                optimum=neighbours[bestIndex]
                optimumScore=newBestCandidateScore
                dry = 0
                print("[%s] ITERATION %d, NEW OPTIMUM! new=%d" % (elapsed(start), iteration, optimumScore))

            bestCandidate = neighbours[bestIndex]
            bestCandidateScore = newBestCandidateScore
            tabu.add(bestCandidate)

            if iteration > maxIterations:
                break
            if dry > maxDryIterations:
                break

    return optimum

def getLibraryScore(used, turn, i):
    # print("TH", used)
    signup = SORTED_LIBRARY_SIGNUPS[i]
    library = SORTED_LIBRARY_INDEXES[i]
    if library in used:
        return 0
    if turn + signup > TURNS:
        return 0
    maxBooks = (TURNS - signup - turn) * RATES[library]
    score = 0
    books = set([])
    for i in range(maxBooks):
        book = LIBRARIES[library].findBestBookIndex(books)

        if book is None:
            break

        score += SCORES[book]
        books.add(book)
    score = score / signup

    return score
def findBestLibraryGreedy(used, turn):

    # print(used)
    # best = None
    # bestScore = 0
    # best = None
    with Pool(THREADS) as p:
        libraryScores = p.starmap(getLibraryScore, [(used, turn, i) for i in range(len(SORTED_LIBRARY_SIGNUPS))])

        bestIx = np.argmax(libraryScores)
        if libraryScores[bestIx] != 0:
            return SORTED_LIBRARY_INDEXES[bestIx]
        else:
            return None


    # for i in range(len(SORTED_LIBRARY_INDEXES)):
    #     signup = SORTED_LIBRARY_SIGNUPS[i]
    #     library = SORTED_LIBRARY_INDEXES[i]
    #     if library in used:
    #         continue
    #     if turn + signup > TURNS:
    #         continue
    #     maxBooks = (TURNS - signup - turn) * RATES[library]
    #     score = 0
    #     books = set([])
    #     for i in range(maxBooks):
    #         book = LIBRARIES[library].findBestBookIndex(books)

    #         if book is None:
    #             break

    #         score += SCORES[book]
    #         books.add(book)
    #     score = score / signup

    #     if (score > bestScore):
    #         best = library
    #         bestScore = score

    # return best

def main():
    global SIGNUP
    global RATES
    global SCORES
    global LIBRARY_BOOKS

    global TURNS

    global LIBRARIES
    global SORTED_LIBRARY_INDEXES
    global SORTED_LIBRARY_SIGNUPS
    global THREADS

    THREADS = 37
    # print(np.concatenate([[0,1],[1,2]]))
    # exit()

    # L = Loader("in/a_example.in")
    L = Loader("in/b_read_on.in")
    # L = Loader("in/c_incunabula.in")
    # L = Loader("in/d_tough_choices.in")
    # L = Loader("in/e_so_many_books.in")
    # L = Loader("in/f_libraries_of_the_world.in")
    print("Data loaded", flush=True)

    SIGNUP = np.array(L.signups, dtype=np.int32)
    RATES = np.array(L.rates, dtype=np.int32)
    SCORES = np.array(L.books, dtype=np.int32)
    LIBRARY_BOOKS = np.array(L.libraries, dtype=np.int32)
    print("Data copied", flush=True)

    TURNS = L.days

    LIBRARIES = np.array([ Library(SIGNUP[i], RATES[i], np.multiply(LIBRARY_BOOKS[i], SCORES)) for i in range(len(RATES)) ])

    SORTED_LIBRARY_INDEXES = np.argsort(SIGNUP)
    SORTED_LIBRARY_SIGNUPS = SIGNUP[SORTED_LIBRARY_INDEXES]
    print("Data preparsed", flush=True)

    # )
    # # exit()
    # i = 0
    turn = 0
    libraries = set([])

    while turn < TURNS:
        library = findBestLibraryGreedy(libraries, turn)
        if library is None:
            break
        turn += SIGNUP[library]
        libraries.add(library)
        print("Found", library, flush=True)

    solution = Solution(np.fromiter(libraries, int, len(libraries)))
    # print(solution.calcScore())
    # exit()


    # solution = Solution(np.array([]))
    # while True:
    # #     # print(i, solution.calcScore(), flush=True)
    #     new = solution.find_add_neighbour()
    #     if new is not None:
    #         solution = new
    #     else:
    #         break


    best = tabuSearch(
        solution,
        THREADS,
        [
            Solution.find_switch_neighbour,
            Solution.find_swap_neighbour,
            Solution.find_add_neighbour
        ],
        [
            # 0, 0.999, 0.001
            0.03, 0.95, 0.02
        ],
        500000000,
        100
    )
    print(best.calcScore())
    print(best.library_indexes)

    Writer(best, SIGNUP, RATES, TURNS, SCORES, L.filename).write()

    # start = time.time()
    # solutions = [solution]
    # for i in range(10):
    #     # solution.calcScore()

    #     # print(time.time() - start, solution.calcScore(), flush=True)
    #     solution = solution.find_swap_neighbour()
    #     solutions.append(solution)
    #     # print(time.time() - start, flush=True)

    # # with Pool(5) as p:
    #     # print(p.map(calcParallelScore, solutions))
    # # solution.calcScore()

    # s1 = Solution([0,1])
    # s2 = Solution([0,1])
    # print(s1==s2)
    # print(hash(s1), hash(s2))

    # print(solution.library_indexes)
    # print(solution.calcScore())
    # print(solution.find_switch_neighbour().library_indexes)


if __name__ == '__main__':
    main()
