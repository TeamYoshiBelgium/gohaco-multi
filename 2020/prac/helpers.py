def score_max(hub):
    return hub.max_slices


def validate_slices(hub, pizzas):
    # print(pizzas)
    slices = 0
    for pizza in pizzas:
        slices += pizza.slices
        
    if(hub.max_slices < slices):
        return False
    return True


def calculate_score(hub, pizzas):
    score = 0
    if not validate_slices(hub, pizzas):
        return -1
    for pizza in pizzas:
        score += pizza.get_score()
    return score


def print_mat(mat):
    for row in mat:
        for cell in row:
            if cell > 9:
                print("" + str(cell) + " ", end="")
            elif cell > 0:
                print(" " + str(cell) + " ", end="")
            else:
                print("" + str(cell) + " ", end="")
        print()
