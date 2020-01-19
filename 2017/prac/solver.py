from domain import SliceClass, PizzaClass


def find_solution(pizza):
    slices = []
    slices_mat = [[-1 for y in range(pizza.length)] for x in range(pizza.width)]
    # print_mat(slices_mat)

    # Fill slices with minimal needed

    get_empty_slice(slices, slices_mat, pizza)
    # print_mat(slices_mat)
    expand_slices(slices, slices_mat, pizza)
    return slices


def expand_slices(slices, slices_mat, pizza):
    for slice in slices:
        slice_score = slice.get_score()
        if slice_score > pizza.max_cells:
            raise RuntimeError("Pizza slice to big!")
        elif slice_score == pizza.max_cells:
            continue
        row_start = slice.row_start
        col_start = slice.col_start
        row_end = slice.row_end
        col_end = slice.col_end
        slice_nr = slice.nr
        result = expand_slice_rec(row_start, col_start, row_end, col_end, slice_nr, slices_mat, pizza)
        if result["score"] > slice_score:
            slice.row_start = result["row_start"]
            slice.col_start = result["col_start"]
            slice.row_end = result["row_end"]
            slice.col_end = result["col_end"]
            for i in range(slice.row_start, slice.row_end + 1):
                for j in range(slice.col_start, slice.col_end + 1):
                    if slices_mat[i][j] == -1 or slices_mat[i][j] == slice_nr:
                        slices_mat[i][j] = slice_nr
                    else:
                        raise RuntimeError()


def expand_slice_rec(row_start, col_start, row_end, col_end, slice_nr, slices_mat, pizza):
    """
        After finding the minimal slices we try to expand it to an maximum.
    """
    score = get_size(row_start, col_start, row_end, col_end)
    if score > pizza.max_cells:
        return {"score": -1, "row_start": row_start, "col_start": col_start, "row_end": row_end, "col_end": col_end}
    if overlap_with_other(slices_mat, row_start, col_start, row_end, col_end, slice_nr):
        return {"score": -1, "row_start": row_start, "col_start": col_start, "row_end": row_end, "col_end": col_end}
    if not valid(pizza, row_start, col_start, row_end, col_end):
        return {"score": -1, "row_start": row_start, "col_start": col_start, "row_end": row_end, "col_end": col_end}
    score_add_row = -1
    score_min_row = -1
    score_add_col = -1
    score_min_col = -1

    next_row = row_end + 1
    if next_row < pizza.width:
        add_row = expand_slice_rec(row_start, col_start, next_row, col_end, slice_nr, slices_mat, pizza)
        score_add_row = add_row["score"]
    next_col = col_end + 1
    if next_col < pizza.length:
        add_col = expand_slice_rec(row_start, col_start, row_end, next_col, slice_nr, slices_mat, pizza)
        score_add_col = add_col["score"]
    prev_row = row_start - 1
    if prev_row >= 0:
        min_row = expand_slice_rec(prev_row, col_start, row_end, col_end, slice_nr, slices_mat, pizza)
        score_min_row = min_row["score"]
    prev_col = col_start - 1
    if prev_col >= 0:
        min_col = expand_slice_rec(row_start, prev_col, row_end, col_end, slice_nr, slices_mat, pizza)
        score_min_col = min_col["score"]

    new_scores = [score_add_row, score_min_row, score_add_col, score_min_col]
    max_score = max(new_scores)
    if max_score < 0:
        return {"score": score, "row_start": row_start, "col_start": col_start, "row_end": row_end,
                "col_end": col_end}
    max_score_type = new_scores.index(max_score)
    if max_score_type == 0:
        return add_row
    elif max_score_type == 1:
        return min_row
    elif max_score_type == 2:
        return add_col
    elif max_score_type == 3:
        return min_col
    else:
        raise RuntimeError()


def get_empty_slice(slices, slices_mat, pizza):
    for row in range(pizza.width):
        for col in range(pizza.length):
            if slices_mat[row][col] == -1:
                row_start = row
                col_start = col
                row_end = row
                col_end = col
                get_empty_slice_rec(slices, slices_mat, pizza, row_start, col_start, row_end, col_end, 0)


def get_empty_slice_rec(slices: list, slices_mat: list, pizza: PizzaClass, row_start: int, col_start: int, row_end: int,
                        col_end: int, depth: int) -> int:
    """
        Find an minimal empty slice and give back the slice nr. If there is no slice found give back -1.
        We find this by using an recursive search strategy.
    """
    if get_size(row_start, col_start, row_end, col_end) > pizza.max_cells:
        return -1
    if overlap(slices_mat, row_start, col_start, row_end, col_end):
        return -1
    elif valid(pizza, row_start, col_start, row_end, col_end):
        nr = len(slices)
        slices.append(SliceClass(row_start, row_end, col_start, col_end, nr))
        for i in range(row_start, row_end + 1):
            for j in range(col_start, col_end + 1):
                slices_mat[i][j] = nr
        return nr
    else:
        if depth % 2 == 0:
            next_row = row_end + 1
            if next_row < pizza.width:
                nr = get_empty_slice_rec(slices, slices_mat, pizza, row_start, col_start, next_row, col_end, depth + 1)
                if nr >= 0:
                    return nr
            next_col = col_end + 1
            if next_col < pizza.length:
                return get_empty_slice_rec(slices, slices_mat, pizza, row_start, col_start, row_end, next_col, depth + 1)
            return -1
        else:
            next_col = col_end + 1
            if next_col < pizza.length:
                nr = get_empty_slice_rec(slices, slices_mat, pizza, row_start, col_start, row_end, next_col, depth + 1)
                if nr >= 0:
                    return nr
            next_row = row_end + 1
            if next_row < pizza.width:
                return get_empty_slice_rec(slices, slices_mat, pizza, row_start, col_start, next_row, col_end, depth + 1)
            return -1


def get_size(row_start, col_start, row_end, col_end):
    return (abs(row_end - row_start) + 1) * (abs(col_end - col_start) + 1)


def overlap(slices_mat, row_start, col_start, row_end, col_end):
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            if slices_mat[i][j] != -1:
                return True
    return False


def overlap_with_other(slices_mat, row_start, col_start, row_end, col_end, nr):
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            if slices_mat[i][j] != -1 and slices_mat[i][j] != nr:
                return True
    return False


def valid(pizza, row_start, col_start, row_end, col_end):
    M = 0
    T = 0
    for i in range(row_start, row_end + 1):
        for j in range(col_start, col_end + 1):
            piece = pizza[i][j]
            if piece == "M":
                M += 1
            elif piece == "T":
                T += 1
            else:
                raise ValueError
    if (M >= pizza.min_ingredient) and (T >= pizza.min_ingredient):
        return True
    else:
        return False
