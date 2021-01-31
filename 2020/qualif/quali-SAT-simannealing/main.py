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

    L = Loader("in/d_tough_choices.in", 0.0001)

    print("Script v%s started [%s]" % (S.version, L.filename))
    # L.O.optimize2()
    L.O.optimize3()
    W = Writer(L)
    W.write()

if __name__ == '__main__':
    main()
