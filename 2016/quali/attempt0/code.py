import copy
import time


class Map:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.map = []
        row = []
        for j in range(columns):
            row.append("")
        for i in range(rows):
            self.map.append(copy.copy(row))

    def __getitem__(self, key):
        return self.map[key]

    def __str__(self):
        line = 0
        string = ""
        for i in self.map:
            string += (str(line) + ":")
            for j in i:
                string += (" " + j + " ")
            string += "\n"
            line += 1
        return string


def distance(r1, c1, r2, c2):
    return ((abs(r1 - r2)) ** 2 + (abs(c1 - c2) ** 2)) ** (1 / 2)


class Products:
    def __init__(self, id_in, weight):
        self.id = id_in
        self.weight = weight

    def __str__(self):
        string = str(self.id) + " : " + str(self.weight)
        return string

    def __repr__(self):
        return str(self.id)

    def __eq__(self, other):
        return repr(self) == repr(other)


class Cargo:
    def __init__(self, list_in):
        self.store(list_in)
        self.items = dict()
        self.store(list_in)

    def store(self, list_in):
        for i in list_in:
            if i in self.items:
                self.items[i] += 1
            else:
                self.items[i] = 1

    def count(self, item):
        if item in self.items:
            return self.items[repr(item)]
        else:
            return 0

    def remove(self, item):
        if item in self.items:
            if self.items[repr(item)] > 1:
                self.items[repr(item)] -= 1
                return self.items[repr(item)]
            else:
                return ValueError
        else:
            raise ValueError

    def empty(self):
        for i in self.items:
            if self.items[i] > 0:
                return False
        return True

    def contains(self, list_in):
        for i in list_in:
            if self.count(i) < 1:
                return False
        return True


class Warehouses(Cargo):
    def __init__(self, x, y, list_in):
        self.x = x
        self.y = y
        super.__init__(list_in)


class Orders(Cargo):
    def __init__(self, x, y, items):
        self.x = x
        self.y = y
        self.fulfilled = -1
        self.store(list)


class Drone(Cargo):
    def __init__(self, x, y, max_load):
        self.max_load = max_load
        self.load = 0
        self.wait = 0
        self.x = x
        self.y = y

    def turn(self):
        if self.wait > 0:
            self.wait -= 1

    def fly_to(self, new_x, new_y):
        self.wait = distance(x, y, new_x, new_y)

    def load(self, list, warehouse):
        total_weight = 0
        for i in list:
            total_weight += i.weight
        if (total_weight + self.load) > self.max_load:
            return ValueError
        fly_to(warehouse.x, warehouse.y)
        self.store(list)
        self.load += total_weight

    def unload(self, list, warehouse):

    def deliver(self, list, order):
        if self.contain(list):
            fly_to(order.x, order.y)
            self.remove(list)
            order.remove(list)

        else:
            raise ValueError

    def wait(self, time):
        self.wait += time


def read_input(filename):
    f = open("input/" + filename + ".in")
    line = f.readline()
    rows, colums, min_ingredient, max_cells = line.strip().split(" ")
    mat = []
    for line in f:
        row = []
        for i in line.strip():
            row.append(i)
        mat.append(row)
    piza = pizaClass(mat, min_ingredient, max_cells)
    f.close()
    return rows, colums, min_ingredient, max_cells, piza


def score(slices):
    s = 0
    for i in slices:
        s += len(i)
    return s


def print_mat(mat):
    for x in mat:
        for y in x:
            if (y > 9):
                print("" + str(y) + " ", end="")
            elif (y > 0):
                print(" " + str(y) + " ", end="")
            else:
                print("" + str(y) + " ", end="")
        print()


def mat_solved(mat):
    solved = True
    for a in mat:
        for b in a:
            if (b == -1):
                solved = False
                # if(solved):
                # print("Opgelost")
    return solved


def slice_solved(slices):
    global score_max_piza
    if (score(slices) == score_max_piza):
        return True
    else:
        return False


score_max = 0
slices_max = []
mat_max = []


def find_solution(slices, mat, max_cells, piza, slices_ignore):
    global score_max, slices_max, mat_max
    row = 0
    col = 0
    count = 0

    for x in mat:
        col = 0
        for y in x:
            if (y == -1):
                for i in range(1, (max_cells + 1)):
                    for j in range(1, (max_cells // i + 1)):
                        try:
                            slice = piza.piece(row, col, i, j)
                        except IndexError:
                            # print("er r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))
                            continue
                        else:
                            if (slice.valid()):

                                already_use = False
                                mat_new = copy.deepcopy(mat)
                                # print(slice)
                                # print(piza)
                                if slice in slices_ignore:
                                    # print(repr(slice))
                                    # print(slices_ignore)
                                    continue
                                for k in range(i):
                                    for l in range(j):
                                        # print("t " + str(row) + " " + str(col))
                                        # print("t2 " + str(l) + " " + str(k))
                                        if (mat[l + row][k + col] != -1):
                                            # print("Al gesneden")
                                            already_use = True
                                            break

                                        mat_new[l + row][k + col] = len(slices) + 1
                                    if (already_use):
                                        break

                                if (not already_use):

                                    slices_new = copy.copy(slices)
                                    slices_new.append(slice)

                                    # print(len(slices))
                                    # print_mat(mat_new)
                                    # print("r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))
                                    if (score(slices_new) > score_max):
                                        score_max = score(slices_new)
                                        slices_max = slices_new
                                        mat_max = mat_new
                                        print("Score temp " + str(max_cells) + " : " + str(score(slices_max)))
                                        write_solution(slices_max, str(max_cells))
                                        # print_mat(mat_new)
                                        print()
                                    if (slice_solved(slices_new)):
                                        return slices_new, mat_new
                                    slices_new, mat_new = find_solution(slices_new, mat_new, max_cells, piza,
                                                                        copy.copy(slices_ignore))
                                    if (slice_solved(slices_new)):
                                        return slices_new, mat_new
                                    slices_ignore.append(slice)
                                    # else:
                                    # print("val r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))

            col += 1
        row += 1
    # print("TEST")
    return slices, mat


def write_solution(slices, filename):
    f = open("output/" + filename + ".out", "w")
    f.write(str(len(slices)))
    for i in slices:
        f.write("\n")
        f.write(str(i.x) + " " + str(i.y) + " " + str(i.x + i.width - 1) + " " + str(i.y + i.length - 1))
    f.close()


if __name__ == "__main__":
    # filename = "busy_day"
    # filename = "redundancy"
    filename = "mother_of_all_warehouses"
    map, products, warehouses, orders, drones = read_input(filename)

    print(rows, colums, min_ingredient, max_cells)
    print(piza)
    slices = []
    mat = []
    for i in range(int(rows)):
        colum = []
        for j in range(int(colums)):
            colum.append(-1)
        mat.append(colum)

    start_time = time.time()
    slices_ignore = []
    slices, mat = find_solution(slices, mat, int(max_cells), piza, slices_ignore)
    print("--- %s seconds ---" % (time.time() - start_time))
    print_mat(mat)
    write_solution(slices_max, filename)

    # print(piza.piece(4,1,3,2))
    # print(piza.piece(4,1,3,2).valid())
    print("Score: " + str(score(slices_max)))
