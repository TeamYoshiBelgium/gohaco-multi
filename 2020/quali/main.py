# Copyright (C) Johannes Bergé - All Rights Reserved
# Unauthorized copying, editing or redistribution of this
# file or any file in the project is strictly and
# unconditionally prohibited, irrespective of the medium
# or intention of the executed action.
# Proprietary and confidential.


from classes.Settings import Settings
from classes.Loader import Loader
from classes.Writer import Writer


def main():
    S = Settings()
    print("Script v%s started" % S.version)

    # L = Loader("in/busy_day.in")
    # L = Loader("in/mother_of_all_warehouses.in")
    # L = Loader("in/redundancy.in")
    # L = Loader()
    W = Writer(L)
    W.write()

if __name__ == '__main__':
    main()
