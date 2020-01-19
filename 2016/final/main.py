# Copyright (C) Johannes Bergé - All Rights Reserved
# Unauthorized copying, editing or redistribution of this
# file or any file in the project is strictly and
# unconditionally prohibited, irrespective of the medium
# or intention of the executed action.
# Proprietary and confidential.

import sys

from classes.Settings import Settings
from classes.Loader import Loader
from classes.Writer import Writer
from classes.Drawer import Drawer


def main():
    S = Settings()
    print("Script v%s started" % S.version)

    if (len(sys.argv) > 1):
        L = Loader(sys.argv[1])
    else:
        # L = Loader("in/mother_of_all_warehouses.in")
        L = Loader("in/busy_day.in")
        # L = Loader("in/redundancy.in")
        # L = Loader("in/example.in")

    L.O.optimize()
    # D = Drawer(L.O)

    W = Writer(L)
    W.write()

    L.O.applySimpleTSP()

    W = Writer(L, ".tsp")
    W.write()

if __name__ == '__main__':
    main()
