import sys

line = 0
stdin = sys.stdin.readlines()
def cin():
    global line
    # print(stdin[line].strip())
    lst = [ int(x) if x.isdigit() else x for x in stdin[line].strip().split(" ") ]
    line += 1
    return lst[0] if len(lst) == 1 else lst

def solve():
    N, B = cin()
    ans = 0
    costs = cin()
    costs = sorted(costs)
    i = 0
    while i < N:
        c = costs[i]
        if ans + c <= B:
            ans += c
        else:
            break

        i+= 1

    return i

def main():
    n = cin()
    buf = []
    for case in range(n):
        buf.append("Case #%i: %s" % (case+1, str(solve())))

    for item in buf:
        print(item)

main()
