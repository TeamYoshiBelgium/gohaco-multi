import heapq

class Engine:
    def __init__(self, heuristic, projects, persons):
        self.heuristic = heuristic
        self.projects = projects
        self.persons = persons
        self.projectCount = len(projects)
        self.personCount = len(persons)

        self.planned_projects = []


    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)

        for project in projects:
            # for skill in project.skills:
            candidates = []


            remainingSkills = [skill for skill in project.skills]

            while remainingSkills:
                personScores = []
                skillMentorLevels = {}

                for person in self.persons:
                    if (person.time + project.duration) > project.before:
                        continue

                    score = 0
                    for skill in project.skills:
                        if skill in person.skills:
                            if project.skills[skill] < person.skills[skill]:
                                score += 1
                            # Learning yourself
                            elif project.skills[skill] == person.skills[skill]:
                                score += 2
                            # Learning by being mentored
                            elif project.skills[skill] - 1 == person.skills[skill] and skill in skillMentorLevels and skillMentorLevels[skill] >= project.skills[skill]:
                                score += 2.5

                    # TODO Correction: maximum possible score remaining instead of project score
                    timeFactor = (project.score - min(0, project.before - (person.time + project.duration)))/project.score


                    heapq.heappush(personScores, (-score * timeFactor, person))

                print(personScores)

                break
        print("GREEDY")

    def improve(self):
        print("IMPROVE")