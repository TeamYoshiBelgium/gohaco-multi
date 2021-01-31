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

    # L = Loader("in/a_example.in", 1, 0.5)
    # L = Loader("in/b_read_on.in", 1.2, 0.7)# 0, 1, 0, 2, 1)
    L = Loader("in/c_incunabula.in", 1, 1)# 0.5, 1, 10, 0.2, 1)
    # L = Loader("in/d_tough_choices.in", 1, 0)# 0.5, 1, 2, 0.1, 1)
    # L = Loader("in/e_so_many_books.in", 0.8, 2)# 0.1, 1, 2, 1, 1)
    # L = Loader("in/f_libraries_of_the_world.in", 0.6, 0.5)# 0.1, 0.65, 4, 0, 1)
    # L = Loader()

    print("Script v%s started [%s]" % (S.version, L.filename))
    L.O.optimize2()
    W = Writer(L)
    W.write()

if __name__ == '__main__':
    main()
