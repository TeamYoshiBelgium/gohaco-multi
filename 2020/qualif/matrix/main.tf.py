# Copyright (C) Johannes Berge - All Rights Reserved
# Unauthorized copying, editing or redistribution of this
# file or any file in the project is strictly and
# unconditionally prohibited, irrespective of the medium
# or intention of the executed action.
# Proprietary and confidential.
import time
import random
import numpy as np
import tensorflow as tf

import scipy as sp
from scipy import optimize
from classes.Loader import Loader



# def main():
#     dim = 10000
#     it = 10

#     a = np.random.rand(dim,dim)
#     b = np.random.rand(dim,dim)
#     c = None
#     start = time.time()
#     for i in range(it):
#         c = np.multiply(a,b)
#     print("Numpy:", time.time()-start)
#     # print(c)
#     start = time.time()
#     for i in range(it):
#         c = tf.math.multiply(a,b)
#     print("Tensor:", time.time()-start)
#     # print(c)
#     start = time.time()
#     print("done")

LIBRARIES = 10000
BOOKS = 10000
MAX_RATE=2
TURNS = 1000

BOOKS_PER_LIBRARY = 50

LIBRARY_BOOKS = None
SIGNUP = None
RATES = None
SCORES = None

def randomLibrary():
    a = np.array([1]*BOOKS_PER_LIBRARY + [0]*(BOOKS-BOOKS_PER_LIBRARY))
    np.random.shuffle(a)
    return a

def randomSignup():
    return random.randint(
        round(max(1,TURNS/LIBRARIES)),
        round(max(1,TURNS/LIBRARIES)*2)
    )

def generateRandomPop():
    global TURNS
    global MAX_RATE

    global LIBRARY_BOOKS
    global SIGNUP
    global RATES
    global SCORES

    SIGNUP        = np.array([randomSignup() for lib in range(LIBRARIES)], dtype='i4')
    RATES         = np.array([random.randint(1,MAX_RATE) for lib in range(LIBRARIES)], dtype='i4')
    SCORES        = np.array(list(sorted([random.randint(1,BOOKS) for bk in range(BOOKS)], reverse = True)), dtype='i4')
    LIBRARY_BOOKS = np.array([randomLibrary() for lib in range(LIBRARIES)], dtype='i4')


def main():
    # generateRandomPop()

    print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))


    global LIBRARY_BOOKS
    global SIGNUP
    global RATES
    global SCORES

    global TURNS

    # L = Loader("in/a_example.in")
    # L = Loader("in/b_read_on.in")
    L = Loader("in/f_libraries_of_the_world.in")
    L.sortBooks()

    SIGNUP = L.signups
    RATES = L.rates
    SCORES = L.books
    LIBRARY_BOOKS = L.libraries

    TURNS = L.days

    # calcScore([1.96175873,1.97954047,0.62813779,0.73641087,-0.73968077,0.15938987,0.95334414,0.08776266])


    # opt = tfp.optimizer.nelder_mead_minimize(
    #     calcScore,
    #     initial_vertex=heuristics,
    #     max_iterations=1000,
    #     func_tolerance=1e-8,
    #     position_tolerance=1e-8,
    # )\

    # scoreFactor=0.5
    # scorePow=1.
    # remainingFactor=0
    # remainingPow=0.5
    # minSignupFactor=-0.5
    # minSignupPow=1.
    # avgSignupFactor=-0.5
    # avgSignupPow=2.

    # print(SIGNUP)

    result = sp.optimize.differential_evolution(
        calcScore,
        # [scoreFactor,scorePow,remainingFactor,remainingPow,minSignupFactor,minSignupPow,avgSignupFactor,avgSignupPow],
        [
            (0,2),
            (0,2),
            (0,1),
            (0,1),
            (-1,1),
            (0,1),
            (-1,1),
            (0,1)
        ],
        strategy='best1bin',
        # updating='deferred',
        # method='Powell',
        callback=lambda x0, **kargs: print("\n\nBest: %d, convergence: %f, heuristics: %s\n" % (-calcScore(x0), kargs['convergence'], x0)),
        popsize=4,
        # init=(1,[scoreFactor, scorePow, remainingFactor, remainingPow, minSignupFactor, minSignupPow, avgSignupFactor, avgSignupPow]),
        workers=30
    )
    print("")
    print("Result 1: %02f - iterations: %d" % (result.fun, result.nit))
    print(result.x)
    print("")
    # print("======================================================================")
    # print("")


def clearBooks(libraries, clearIndex, clearBookCount):
    i = 0
    col = 0
    result = []
    for element in libraries[clearIndex]:
        if element == 1:
            libraries[:,col] = 0
            result.append(col)
            i=i+1
        if i == clearBookCount:
            break
        col += 1
    libraries[clearIndex,:] = 0
    return result

def calcScore(heuristics_arr):
    global TURNS
    global LIBRARY_BOOKS
    global SIGNUP
    global RATES
    global SCORES

    start_time = time.time()

    turn = 0
    maxturns = TURNS

    available = LIBRARY_BOOKS.copy()
    library_signups = SIGNUP.copy()
    library_rates = RATES.copy()
    book_scores = SCORES.copy()
    # print(available)

    # available = np.array([
    #         [0,1,0,0,1,0,1,1,0,1,0,1,0,0,1],
    #         [1,1,0,1,0,0,1,1,0,1,0,1,0,0,1],
    #         [0,1,1,0,0,1,1,0,0,0,1,1,0,1,0],
    #         [0,1,1,0,0,1,1,0,1,1,1,0,0,1,0]
    # ])
    # book_scores = np.array([140,140,120,110,100,90,80,70,60,60,40,30,30,20,10])
    # library_signups = np.array([3,2,2,4])
    # library_rates = np.array([2,1,1,1])

    result = {}

    tensorTurn = tf.Variable(turn, dtype=tf.float32)
    tensorMaxturns = tf.Variable(maxturns, dtype=tf.float32)
    tensorAvailable = tf.Variable(available, dtype=tf.float32)
    tensorBook_scores = tf.Variable(book_scores, dtype=tf.float32)
    tensorLibrary_signups = tf.Variable(library_signups, dtype=tf.float32)
    tensorLibrary_rates = tf.Variable(library_rates, dtype=tf.float32)
    tensorHeuristics_arr = tf.Variable(heuristics_arr, dtype=tf.float32)

    bestIndex = findBestLibraryIndexTf(
        tensorTurn,
        tensorMaxturns,
        tensorAvailable,
        tensorBook_scores,
        tensorLibrary_signups,
        tensorLibrary_rates,
        tensorHeuristics_arr
    )
    while (bestIndex.numpy() >= 0):
        turn += library_signups[bestIndex.numpy()]
        result[bestIndex.numpy()] = clearBooks(available, bestIndex.numpy(), (maxturns-turn)*library_rates[bestIndex.numpy()])

        bestIndex = findBestLibraryIndexTf(
            turn,
            maxturns,
            available,
            book_scores,
            library_signups,
            library_rates,
            heuristics_arr
        )

    score = 0
    for key in result:
        for book in result[key]:
            score += book_scores[book]

    # if ITERATION % 50 == 0:
    elapsed_time = time.time() - start_time
    print("Score=%d, elapsed=%.02f, heuristics=%s" % (score, elapsed_time, [round(x, 2) for x in heuristics_arr]), flush=True)

    # print("%d," % score, end='', flush=True)


    return -score*1.

@tf.function(input_signature=(
    tf.TensorSpec(shape=(), dtype=tf.float32),
    tf.TensorSpec(shape=(), dtype=tf.float32),
    tf.TensorSpec(shape=(None,None,), dtype=tf.float32),
    tf.TensorSpec(shape=(None,), dtype=tf.float32),
    tf.TensorSpec(shape=(None,), dtype=tf.float32),
    tf.TensorSpec(shape=(None,), dtype=tf.float32),
    tf.TensorSpec(shape=(None,), dtype=tf.float32)
))

def findBestLibraryIndexTf(turn,maxturns,available,book_scores,library_signups,library_rates,heuristics_arr):
    # @tf.function
    # def tf_repeat(availability, values):
    #     print("disableOutOfTimeBooks")
    #     return tf.linalg.matmul(
    #         tf.linalg.diag(values),
    #         tf.transpose(tf.ones(availability.shape))
    #     )
        # shape = tf.shape_n(values)
        # rng = tf.range(shape[0][0])
        # indices = tf.repeat(rng, repeats)
        # return tf.gather(values, indices, axis=axis)

    @tf.function
    def disableOutOfTimeBooks(availability, availableTurnsPerLibrary):
        return tf.math.multiply(
            tf.transpose(tf.map_fn(
                lambda x: tf.where(
                    x < availableTurnsPerLibrary,
                    tf.constant(1, dtype=tf.float32),
                    tf.constant(0, dtype=tf.float32)
                ),
                tf.transpose(tf.math.cumsum(availability, 1))
            )),
            availability
        )

    @tf.function
    def availableTurns(library_signups, currentTurn, totalTurns):
        return tf.math.maximum(library_signups*(-1) + totalTurns - currentTurn, 0)

        # return np.multiply(np.where(np.cumsum(vec) <= num, np.ones(vec.size, dtype=np.int8), 0), vec)

    def zeroToOne(num):
        if num == 0:
            return tf.constant(1, dtype=tf.float32)
        return num

    @tf.function
    def calculatedBookHeuristicMatrix(
            book_normalizedScores,
            book_remainingLibraryCountsSigmoid,
            book_normalizedMinSignupTimes,
            book_normalizedAverageLibrarySignupTimes,
            scoreFactor=1,
            scorePow=1,
            remainingFactor=0.5,#-0.5,
            remainingPow=0.5,
            minSignupFactor=-0.5,#-1,
            minSignupPow=1,
            avgSignupFactor=-0.5,#-0.2,
            avgSignupPow=2
        ):
        return (
            tf.math.multiply(
                scoreFactor,
                tf.pow(
                    book_normalizedScores,
                    zeroToOne(scorePow)
                )
            ) +
            tf.math.multiply(
                remainingFactor,
                tf.pow(
                    book_remainingLibraryCountsSigmoid,
                    zeroToOne(remainingPow)
                )
            ) +
            tf.math.multiply(
                minSignupFactor,
                tf.pow(
                    book_normalizedMinSignupTimes,
                    zeroToOne(minSignupPow)
                )
            ) +
            tf.math.multiply(
                avgSignupFactor,
                tf.pow(
                    book_normalizedAverageLibrarySignupTimes,
                    zeroToOne(avgSignupPow)
                )
            )
        )

    ##########################################################################
    ##########################################################################
    ##########################################################################
    start_time = time.time()

    scoreFactor     = heuristics_arr[0]
    scorePow        = heuristics_arr[1]
    remainingFactor = heuristics_arr[2]
    remainingPow    = heuristics_arr[3]
    minSignupFactor = heuristics_arr[4]
    minSignupPow    = heuristics_arr[5]
    avgSignupFactor = heuristics_arr[6]
    avgSignupPow    = heuristics_arr[7]

    maxSignup = tf.reduce_max(library_signups)
    maxScore = tf.reduce_max(book_scores)

    book_signupsPerLibrary = tf.math.multiply(tf.transpose(available), library_signups)
    book_normalizedScores = tf.math.divide(book_scores, maxScore)
    book_remainingLibraryCounts = tf.math.reduce_sum(available, 0)

    book_remainingLibraryCountsNormalized = 1/(1+book_remainingLibraryCounts)

    book_normalizedMinSignupTimes = tf.math.divide(
        tf.math.reduce_min(
            tf.where(tf.equal(book_signupsPerLibrary, 0), maxSignup, book_signupsPerLibrary),
            1
        ),
        maxSignup
    )

    book_normalizedAverageLibrarySignupTimes = tf.divide(
        tf.math.reduce_sum(
            book_signupsPerLibrary,
            1
        ),
        tf.where(
            tf.equal(
                book_remainingLibraryCounts,
                0
            ),
            tf.constant(1, dtype=tf.float32),
            tf.math.multiply(
                book_remainingLibraryCounts,
                maxSignup
            ),
        )
    )


    # print("EL7:", time.time() - start_time)


    # # for i in range(book_normalizedScores.size):
    # #     print("(%.2f, %.2f, %.2f, %.2f)" % (
    # #         book_normalizedScores[i],
    # #         book_remainingLibraryCountsSigmoid[i],
    # #         book_normalizedMinSignupTimes[i],
    # #         book_normalizedAverageLibrarySignupTimes[i]
    # #     ))


    # scannableBookScoreMatrix = None
    # print("EL8:", time.time() - start_time)
    # print(disableOutOfTimeBooks(
    #         available,
    #         availableTurns(library_signups, turn, maxturns)
    #     ))
    scannableBookScoreMatrix = tf.math.multiply(
        disableOutOfTimeBooks(
            available,
            availableTurns(library_signups, turn, maxturns)
        ),
        calculatedBookHeuristicMatrix(
            book_normalizedScores,
            book_remainingLibraryCountsNormalized,
            book_normalizedMinSignupTimes,
            book_normalizedAverageLibrarySignupTimes,
            scoreFactor,
            scorePow,
            remainingFactor,
            remainingPow,
            minSignupFactor,
            minSignupPow,
            avgSignupFactor,
            avgSignupPow
        )
    )
    # print("EL9:", time.time() - start_time)
    scoreSums = tf.reduce_sum(scannableBookScoreMatrix, axis=1)

    if (tf.reduce_max(scoreSums) == 0):
        return tf.constant(-1, dtype=tf.int64)
    else:
        return tf.argmax(scoreSums)


def findBestLibraryIndex(
        turn,
        maxturns,
        available,
        book_scores,
        library_signups,
        library_rates,
        heuristics_arr,
        start_time
    ):

    def disableOutOfTimeBooks(availability, availableTurnsPerLibrary):
        return np.multiply(
            np.where(
                np.cumsum(
                    availability, 1) <= np.transpose(
                        np.repeat(
                            np.array([availableTurnsPerLibrary]),
                            availability.shape[1],
                            axis=0
                        )
                    ),
                1,
                0
            ),
            availability
        )

    def availableTurns(library_signups, currentTurn, totalTurns):
        return np.maximum(library_signups*(-1) + totalTurns - currentTurn, 0)

        # return np.multiply(np.where(np.cumsum(vec) <= num, np.ones(vec.size, dtype=np.int8), 0), vec)

    def nanToOne(vec):
        return 1-np.nan_to_num(1-vec)

    def zeroToOne(num):
        if num == 0:
            return 1
        return num

    def calculatedBookHeuristicMatrix(
            book_normalizedScores,
            book_remainingLibraryCountsSigmoid,
            book_normalizedMinSignupTimes,
            book_normalizedAverageLibrarySignupTimes,
            scoreFactor=1,
            scorePow=1,
            remainingFactor=0.5,#-0.5,
            remainingPow=0.5,
            minSignupFactor=-0.5,#-1,
            minSignupPow=1,
            avgSignupFactor=-0.5,#-0.2,
            avgSignupPow=2
        ):
        return np.nan_to_num(
            scoreFactor     * (book_normalizedScores                    ** zeroToOne(scorePow     )) +
            remainingFactor * (book_remainingLibraryCountsSigmoid       ** zeroToOne(remainingPow )) +
            minSignupFactor * (book_normalizedMinSignupTimes            ** zeroToOne(minSignupPow )) +
            avgSignupFactor * (book_normalizedAverageLibrarySignupTimes ** zeroToOne(avgSignupPow ))
        )

    scoreFactor     = heuristics_arr[0]
    scorePow        = heuristics_arr[1]
    remainingFactor = heuristics_arr[2]
    remainingPow    = heuristics_arr[3]
    minSignupFactor = heuristics_arr[4]
    minSignupPow    = heuristics_arr[5]
    avgSignupFactor = heuristics_arr[6]
    avgSignupPow    = heuristics_arr[7]

    print("EL1:", time.time() - start_time)
    maxSignup = np.max(library_signups)
    maxScore = np.max(book_scores)
    print("EL1B:", time.time() - start_time)
    transpose = np.transpose(available)
    print("EL1C:", time.time() - start_time)
    book_signupsPerLibrary = np.multiply(transpose, library_signups)
    print("EL2:", time.time() - start_time)
    book_normalizedScores = np.divide(book_scores, maxScore)
    print("EL3:", time.time() - start_time)
    book_remainingLibraryCounts = np.sum(available, axis=0)
    print("EL4:", time.time() - start_time)
    # book_remainingLibraryCountsSigmoid = -2/(1+np.exp(-book_remainingLibraryCounts))+2
    book_remainingLibraryCountsNormalized = 1/(1+book_remainingLibraryCounts)
    print("EL5:", time.time() - start_time)
    book_normalizedMinSignupTimes = np.divide(
        np.min(
            book_signupsPerLibrary,
            axis=1,
            initial=maxSignup,
            where=book_signupsPerLibrary != 0
        ),
        maxSignup
    )
    print("EL6:", time.time() - start_time)
    book_normalizedAverageLibrarySignupTimes = None
    with np.errstate(divide='ignore', invalid='ignore'):
        book_normalizedAverageLibrarySignupTimes = np.divide(
            np.divide(
                np.sum(
                    np.multiply(
                        np.transpose(available),
                        library_signups
                    ),
                    axis=1
                ),
                book_remainingLibraryCounts
            ),
            maxSignup
        )
    print("EL7:", time.time() - start_time)


    # for i in range(book_normalizedScores.size):
    #     print("(%.2f, %.2f, %.2f, %.2f)" % (
    #         book_normalizedScores[i],
    #         book_remainingLibraryCountsSigmoid[i],
    #         book_normalizedMinSignupTimes[i],
    #         book_normalizedAverageLibrarySignupTimes[i]
    #     ))


    scannableBookScoreMatrix = None
    print("EL8:", time.time() - start_time)
    scannableBookScoreMatrix = np.multiply(
        disableOutOfTimeBooks(
            available,
            availableTurns(library_signups, turn, maxturns)
        ),
        calculatedBookHeuristicMatrix(
            book_normalizedScores,
            book_remainingLibraryCountsNormalized,
            book_normalizedMinSignupTimes,
            book_normalizedAverageLibrarySignupTimes,
            scoreFactor,
            scorePow,
            remainingFactor,
            remainingPow,
            minSignupFactor,
            minSignupPow,
            avgSignupFactor,
            avgSignupPow
        )
    )
    print("EL9:", time.time() - start_time)
    scoreSums = np.sum(scannableBookScoreMatrix, axis=1)
    if (np.max(scoreSums) == 0):
        return None
    else:
        return np.argmax(scoreSums)

if __name__ == '__main__':
    main()
