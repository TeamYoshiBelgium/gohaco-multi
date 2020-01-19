from domain import *


def read_input(input_file):
    f = open(input_file)
    line = f.readline()
    rows, colums, min_ingredient, max_cells = line.strip().split(" ")
    mat = []
    for line in f:
        row = []
        for i in line.strip():
            row.append(i)
        mat.append(row)
    pizza = PizzaClass(mat, int(min_ingredient), int(max_cells))
    f.close()
    return pizza
