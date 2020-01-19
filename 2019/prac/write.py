def write_solution(pizzas, filename):
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(pizzas)))
    f.write("\n")
    pizzas = sorted(pizzas, key=lambda x: x.type, reverse=False)
    for pizza in pizzas:
        f.write(str(pizza.type) + " ")
    f.close()
