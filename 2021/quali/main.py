import sys

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    if len(sys.argv) > 1 and sys.argv[1] != "-a":
        execute_file(sys.argv[1])
    else:
        execute_file("in/a.txt")
        # execute_file("in/b.txt")
        # execute_file("in/c.txt")
        # execute_file("in/d.txt")
        # execute_file("in/e.txt")
        # execute_file("in/f.txt")


def execute_file(file_name):
    S = Settings()
    print("Script v%s started [%s]" % (S.version, file_name))

    L = Loader(file_name)

    L.O.optimize()

    W = Writer(L, L.O)
    W.write()

if __name__ == '__main__':
    main()
