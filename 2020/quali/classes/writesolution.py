import os


def write_solution(orderedLibraries, filename):
    score = 0
    if not os.path.isdir("output"):
        os.mkdir("output")
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(orderedLibraries)))
    f.write("\n")
    for library in orderedLibraries:
        f.write(str(library.id) + " " + str(len(library.scanned_books)))
        f.write("\n")
        for book in library.scanned_books:
            f.write(str(book.id))
    f.close()
