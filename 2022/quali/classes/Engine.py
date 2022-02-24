class Engine:
    def __init__(self, heuristic, projects, persons):
        self.heuristic = heuristic
        self.projects = projects
        self.persons = persons
        self.projectCount = len(projects)
        self.personCount = len(persons)


    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)
        for project in projects:
            for skill in project.skills:
                for person in self.persons:
                    if(skill in person.skills):
                        # assign sli

        print("GREEDY")

    def improve(self):
        print("IMPROVE")