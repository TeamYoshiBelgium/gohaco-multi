class Engine:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)
        print("GREEDY")

    def improve(self):
        print("IMPROVE")