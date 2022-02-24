class Engine:
    def __init__(self, heuristic):
        self.heuristic = heuristic

    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)
        for project in projects:
            for skill in project.skills:
                for person in self.persons
                    if(skill in person.skills):
                        # assign sli

        print("GREEDY")

    def improve(self):
        print("IMPROVE")