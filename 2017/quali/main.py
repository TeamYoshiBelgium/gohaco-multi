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

def main():
    S = Settings()
    print("Script v%s started" % S.version)

    if (len(sys.argv) > 1):
        L = Loader(sys.argv[1])
    else:
        # L = Loader("in/kittens.in") # 10k vids, 200k reqs, 1000 ep's, 500 srvrs
        # L = Loader("in/example.in")
        L = Loader("in/me_at_the_zoo.in") # 100 vids, 100 reqs, 10 ep's, 10 srvrs
        # L = Loader("in/videos_worth_spreading.in") # 10k vids, 100k reqs, 100 ep's, 100 srvrs
        # L = Loader("in/trending_today.in") # 10k vids, 100k reqs, 100 ep's, 100 srvrs

    L.O.optimize()
    # D = Drawer(L.O)

    W = Writer(L)
    W.write()

    # L.O.applySimpleTSP()

    # W = Writer(L, ".tsp")
    # W.write()

if __name__ == '__main__':
    main()
