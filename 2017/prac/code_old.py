import copy
import time

class pizaClass:
    def __init__(self, inMat, min_ingredient, max_cells):
        self.mat = inMat
        self.length = len(inMat[0])
        self.width = len(inMat)
        self.L = int(min_ingredient)
        self.H = int(max_cells)
        self.len = self.length * self.width
        
    def __str__(self):
        line = 0
        string = ""
        for i in self.mat:
            string += (str(line) + ":")
            for j in i:
                string += (" " + j + " ")
            string += ("\n")
            line += 1
        return string


    def __getitem__(self, key):
        return self.mat[key]

    def __len__(self):
        return self.len
    
    def piece(self, x, y, length, width):
        slice = []
        # print("test")
        # print(self.length)
        # print(x)
        # print(y)
        # print(length)
        # print(width)
        # print("test2")
        if self.length < (y+length):
            # print("Error 1")
            raise IndexError
        if self.width < (x + width):
            raise IndexError
        for i in range(width):
            slice.append(self.mat[x + i][y:y+length])
        return sliceClass(slice, self.L, self.H, x, y)


class sliceClass(pizaClass):
    def __init__(self, inMat, min_ingredient, max_cells, x, y):
        super().__init__(inMat, min_ingredient, max_cells)
        self.x = x
        self.y = y
    def valid(self):
        if len(self) > self.H:
            # print(len(self))
            # print(self.H)
            return False
        else:
            M = 0
            T = 0
            # print(self)
            for i in self.mat:
                for j in i:
                    if (j == "M"):
                        M += 1
                    elif (j == "T"):
                        T += 1
                    else:
                        raise
            # print("?")
            # print(M)
            # print(T)
            # print(self.L)
            if ( (M >= self.L) and (T >= self.L) ):
                # print("dafaq")
                return True
            else:
                return False
    def __eq__(self, other):
        if( (self.x == other.x) and (self.y==other.y) and (self.length == other.length) and (self.width == other.width) ):
            return True
        else:
            return False
    
    def __repr__(self):
        string = ""
        string += str(self.x) + " " + str(self.y) + " " + str(self.length) + " " + str(self.width)
        return string
        
def read_input(filename):
    f =  open("input/" + filename + ".in")
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
            if (y>9):
                print( "" + str(y) + " ", end="")
            elif(y>0):
                print( " " + str(y) + " ", end="")
            else:
                print( "" + str(y) + " ", end="")
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
    if(score(slices) == score_max_piza):
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
                    for j in range(1, (max_cells//i + 1)):
                        try:
                            slice = piza.piece(row,col,i,j)
                        except IndexError:
                            # print("er r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))
                            continue
                        else:
                            if(slice.valid()):
                                
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
                                    if(already_use):
                                        break
                                
                                if(not already_use):

                                    slices_new = copy.copy(slices)
                                    slices_new.append(slice)
                                    
                                    # print(len(slices))
                                    # print_mat(mat_new)
                                    # print("r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))
                                    if( score(slices_new) > score_max):
                                        score_max = score(slices_new)
                                        slices_max = slices_new
                                        mat_max = mat_new
                                        print("Score temp " + str(max_cells) + " : " + str(score(slices_max)))
                                        write_solution(slices_max, str(max_cells))
                                        # print_mat(mat_new)
                                        print()
                                    if(slice_solved(slices_new)):
                                        return slices_new, mat_new
                                    slices_new, mat_new = find_solution(slices_new, mat_new, max_cells, piza, copy.copy(slices_ignore))
                                    if(slice_solved(slices_new)):
                                        return slices_new, mat_new
                                    slices_ignore.append(slice)
                                # else:
                                    # print("val r: "  + str(row) + " c: " + str(col) + " i: " + str(i) + " j:" + str(j) + " s:" + str(len(slices)))
            
            col += 1
        row += 1
    # print("TEST")
    return slices, mat

def write_solution(slices, filename):
    f = open("output/" + filename + ".out","w")
    f.write(str(len(slices)))
    for i in slices:
        f.write("\n")
        f.write(str(i.x) + " " + str(i.y) + " " + str(i.x + i.width - 1) + " " + str(i.y + i.length - 1))
    f.close()

    
score_max_piza = 0
if __name__ == "__main__":
    filename = "big"
    # filename = "medium"
    # filename = "small"
    # filename = "example"
    rows, colums, min_ingredient, max_cells, piza =  read_input(filename)
    score_max_piza = int(rows) * int(colums)
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
    