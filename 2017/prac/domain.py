class PizzaClass:
    def __init__(self, in_mat, min_ingredient, max_cells):
        self.mat = in_mat
        self.length = len(in_mat[0])
        self.width = len(in_mat)
        self.min_ingredient = min_ingredient
        self.max_cells = max_cells

    def __str__(self):
        line = 0
        string = "length: %i width: %i min_ingredient: %i max_cells: %i\n" % \
                 (self.length, self.width, self.min_ingredient, self.max_cells)
        string += "   " + "  ".join([str(x) for x in range(self.length)]) + "\n"
        for i in self.mat:
            string += (str(line) + ":")
            for j in i:
                string += (" " + j + " ")
            string += "\n"
            line += 1
        return string

    def __getitem__(self, key):
        return self.mat[key]

    def __len__(self):
        return self.length


class SliceClass:
    def __init__(self, row_start, row_end, col_start, col_end, nr):
        self.row_start = row_start
        self.row_end = row_end
        self.col_start = col_start
        self.col_end = col_end
        self.nr = nr

    def __str__(self):
        return "%i %i %i %i" % (self.row_start, self.col_start, self.row_end, self.col_end)

    def get_score(self):
        return (abs(self.row_end - self.row_start) + 1) * (abs(self.col_end - self.col_start) + 1)
