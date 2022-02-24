import sys
import os

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-a":
        execute_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        execute_file("in/a.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/b.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/c.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/d.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/e.txt")
        
        # print("="*80,end=os.linesep)
        # execute_file("in/f.txt")


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
