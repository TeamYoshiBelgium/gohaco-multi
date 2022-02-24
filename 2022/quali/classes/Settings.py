
# This is a class that is meant to contain only
# static variables or functions, such that they
# can be used in a global fashion throughout the
# project.

class Settings:
    version = "1"

    # Used for print padding
    width = 80

    heuristics = {
        "a_an_example.in": (100, 20),
        "b_better_start_small.in": (100, 20),
        "c_collaboration.in": (4, 20),
        "d_dense_schedule.in": (3, 20),
        "e_exceptional_skills.in": (1, 20),
        "f_find_great_mentors.in": (1, 20),
    }