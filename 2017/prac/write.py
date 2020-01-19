def write_solution(slices, filename):
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(slices)))
    for slice in slices:
        f.write("\n")
        f.write(str(slice))
    f.close()
