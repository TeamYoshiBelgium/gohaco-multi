import argparse
import os
import time

from read import read_input
from write import write_solution
from solver import find_solution
from helpers import calculate_score


def run(input_file):
    filename = os.path.basename(input_file).split(".")[0]
    pizza = read_input(input_file)
    # print(pizza)
    start_time = time.time()
    slices = find_solution(pizza)
    print("--- %s seconds ---" % (time.time() - start_time))

    score = calculate_score(slices)
    if score < 0:
        raise RuntimeError()
    print("%s Score: %i" % (input_file, score))

    filename = filename + "_" + score
    write_solution(slices, filename)
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="the input file")
    parser.add_argument("-a", "--all", help="test all files", action='store_true')
    args = parser.parse_args()
    all = args.all
    if all:
        score_total = 0
        files = ["example", "small", "medium", "big"]
        for file in files:
            score_total += run("input/" + file + ".in")
        print("Total score: %i" % score_total)
    else:
        input_file = args.input
        run(input_file)
