import os

def write_solution(pizzas, filename):
    if not os.path.isdir("output"):
        os.mkdir("output")
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(pizzas)))
    f.write("\n")
    pizzas = sorted(pizzas, key=lambda x: x.type, reverse=False)
    for pizza in pizzas:
        f.write(str(pizza.type) + " ")
    f.close()
