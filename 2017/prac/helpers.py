def score_max(pizza):
    return pizza.length * pizza.width


def validate_slices(slices):
    piece_dict = {}
    for slice in slices:
        for i in range(slice.row_start, slice.row_end + 1):
            if i not in piece_dict:
                piece_dict[i] = []
            for j in range(slice.col_start, slice.col_end + 1):
                if j in piece_dict[i]:
                    return False
                else:
                    piece_dict[i].append(j)
    return True


def calculate_score(slices):
    score = 0
    if not validate_slices(slices):
        return -1
    for slice in slices:
        score += slice.get_score()
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
