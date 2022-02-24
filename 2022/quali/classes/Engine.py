class Engine:
    def __init__(self, heuristic, projects, persons):
        self.heuristic = heuristic
        self.projects = projects
        self.persons = persons

    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)
        print("GREEDY")

    def improve(self):
        print("IMPROVE")