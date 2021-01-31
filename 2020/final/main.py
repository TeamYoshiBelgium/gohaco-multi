import sys

from classes.Loader import Loader
from classes.Writer import Writer
from classes.Settings import Settings


def main():
    S = Settings()

    if len(sys.argv) > 1:
        L = Loader(sys.argv[1])
    else:
        L = Loader("in/a_example.in")
        L = Loader("in/b_single_arm.in")
        L = Loader("in/d_tight_schedule.in")
        L = Loader("in/e_dense_workspace.in")
        L = Loader("in/f_decentralized.in")

    print("Script v%s started [%s]" % (S.version, L.filename))

    L.O.optimize()

    W = Writer(L, L.O)
    W.write()


if __name__ == '__main__':
    main()
