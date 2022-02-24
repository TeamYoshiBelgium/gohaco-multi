
# This is a class that is meant to contain only
# static variables or functions, such that they
# can be used in a global fashion throughout the
# project.

class Settings:
    version = "1"

    # Used for print padding
    width = 80

    heuristics = {
        "a_an_example.in": (0.5, 0.5),
        "b_better_start_small.in": (0.5, 0.5),
        "c_collaboration.in": (0.5, 0.5),
        "d_dense_schedule.in": (0.5, 0.5),
        "e_exceptional_skills.in": (0.5, 0.5),
        "f_find_great_mentors.in": (0.5, 0.5),
    }