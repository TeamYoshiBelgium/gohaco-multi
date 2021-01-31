from domain import *


def read_input(input_file):
    f = open(input_file)
    line = f.readline()
    max_slices, pizza_types = line.strip().split(" ")
    
    line = f.readline()
    f.close()
    
    slices = line.strip().split(" ")
    pizzas = []
    index = 0
    for slice in slices:
        pizza = Pizza(index, slice)
        pizzas.append(pizza)
        index += 1

    string = "index: %i pizza_types: %i\n" % (index, int(pizza_types))
    print(string)

    hub = Hub(max_slices, pizzas)
    return hub
