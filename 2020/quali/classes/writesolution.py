import os


def write_solution(orderedLibraries, filename):
    if not os.path.isdir("output"):
        os.mkdir("output")
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(orderedLibraries)))
    f.write("\n")
    for library in orderedLibraries:
        f.write(str(library.id) + " " + str(len(library.orderedbooks)))
        f.write("\n")
        for book in library.orderedbooks:
            f.write(str(book.id))
    f.close()
