import sys

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-a":
        execute_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        execute_file("in/a.txt", 0.05, 0.8)
        execute_file("in/b.txt", 0.05, 0.8)
        execute_file("in/c.txt", 0.05, 0.8)
        execute_file("in/d.txt", 0.05, 0.8)
        execute_file("in/e.txt", 0.05, 0.8)
        execute_file("in/f.txt", 0.05, 0.8)


def execute_file(file_name, swap_vs_increment_heuristic, increment_decrement_heuristic):
    S = Settings()
    print("Script v%s started [%s]" % (S.version, file_name))

    L = Loader(file_name, swap_vs_increment_heuristic, increment_decrement_heuristic)

    L.O.optimize()

    W = Writer(L, L.O)
    W.write()

if __name__ == '__main__':
    main()
