import argparse
import os
import time

from read import read_input
from write import write_solution
from solver import find_solution
from helpers import calculate_score, score_max


def run(input_file):
    filename = os.path.basename(input_file).split(".")[0]
    photos = read_input(input_file)
    # print(hub)
    start_time = time.time()
    slideshow = find_solution(photos)
    print("--- %s seconds ---" % (time.time() - start_time))

    score = calculate_score(slideshow)
    max_score =  score_max(photos)
    if score < 0:
        raise RuntimeError()
    print("%s Score: %i of max score: %i" % (input_file, score, max_score))

    filename = filename + "_" + str(score)
    write_solution(slideshow, filename)
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="the input file")
    parser.add_argument("-a", "--all", help="test all files", action='store_true')
    args = parser.parse_args()
    all = args.all
    if all:
        score_total = 0
        files = ["a_example", "b_lovely_landscapes", "c_memorable_moments", "d_pet_pictures", "e_shiny_selfies"]
        for file in files:
            score_total += run("in/" + file + ".txt")
        print("Total score: %i" % score_total)
    else:
        input_file = args.input
        run(input_file)
