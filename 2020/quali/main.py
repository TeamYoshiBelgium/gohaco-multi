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

    # L = Loader("in/a_example.in")
    # L = Loader("in/b_read_on.in")
    # L = Loader("in/c_incunabula.in")
    # L = Loader("in/d_tough_choices.in")
    L = Loader("in/e_so_many_books.in")
    # L = Loader("in/f_libraries_of_the_world.in")
    # L = Loader()
    print(L.filename)
    W = Writer(L)
    W.write()

if __name__ == '__main__':
    main()
