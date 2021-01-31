import sys

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    S = Settings()

    if len(sys.argv) != 2:
        print("No argument provided!")
        exit()

    L = Loader(sys.argv[1])
    O = Optimizer(L)

    print("Script v%s started [%s]" % (S.version, L.filename))
    O.optimize()

    W = Writer(L, O)
    W.write()

if __name__ == '__main__':
    main()
