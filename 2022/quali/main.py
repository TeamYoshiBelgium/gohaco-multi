import sys
import os

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-a":
        execute_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        execute_file("in/a_an_example.in.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/b_better_start_small.in.txt")
        
        # print("="*80,end=os.linesep)
        execute_file("in/c_collaboration.in.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/d_dense_schedule.in.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/e_exceptional_skills.in.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/f_find_great_mentors.in.txt")


def execute_file(file_name):
    S = Settings()
    L = Loader(file_name)

    L.engine.optimize()

    W = Writer(L, L.engine)
    W.write()

    # L.engine.improve()
    # W.write()


if __name__ == '__main__':
    main()
