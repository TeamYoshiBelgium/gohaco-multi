from domain import Hub, Pizza


def find_solution(hub):
    pizzas = []
    slices = 0
    pizzas_by_slices = sorted(hub.pizzas, key=lambda x: x.slices, reverse=True)
    
    for pizza in pizzas_by_slices:
    
        slices += pizza.slices
        if(hub.max_slices < slices):
            break
       
        pizzas.append(pizza)

    return pizzas
