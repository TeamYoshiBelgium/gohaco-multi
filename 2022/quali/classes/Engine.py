import heapq

class Engine:
    def __init__(self, heuristic, projects, persons):
        self.heuristic = heuristic
        self.projects = projects
        self.persons = persons
        self.projectCount = len(projects)
        self.personCount = len(persons)


    def optimize(self):
        projects = sorted(self.projects,key= lambda x : x.order, reverse=False)

        while projects:
            project = projects.pop(0)

            # for skill in project.skills:
            candidates = []


            remainingSkills = [skill for skill in project.skills]
            skillMentorLevels = {}

            while remainingSkills:
                print()
                personScores = []

                for person in self.persons:
                    if (person.time + project.duration) > project.before:
                        continue

                    score = 0
                    for skill in remainingSkills:
                        # print(skill, project.skills[skill], person.skills, skill in person.skills)
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

                    if score == 0:
                        continue

                    heapq.heappush(personScores, (-score * timeFactor, person))

                # We cannot complete this project at this time
                print(project)
                if not personScores:
                    print("CANNOT COMPLETE PROJECT")
                    # TODO: re-add, but find termination conditions?
                    break

                print(personScores)

                bestPerson = heapq.heappop(personScores)[1]
                bestSkill = None

                print("PRSN",bestPerson.skills)
                print("PROJ",project.skills)
                print("REMAINING",remainingSkills)
                for skill in sorted(remainingSkills, key=lambda skill: project.skills[skill], reverse=True):
                    print(skill, skill in bestPerson.skills)
                    if skill not in bestPerson.skills:
                        continue

                    qualified = (project.skills[skill] <= bestPerson.skills[skill])
                    mentored = (project.skills[skill] - 1 == bestPerson.skills[skill] and skill in skillMentorLevels and skillMentorLevels[skill] >= project.skills[skill])
                    print(skill, qualified, mentored)
                    if qualified or mentored:
                        bestSkill = skill
                        break

                for skill in bestPerson.skills:
                    skillLevel = 0
                    if skill in skillMentorLevels:
                        skillLevel = skillMentorLevels[skill]

                    skillMentorLevels[skill] = max(skillLevel, bestPerson.skills[skill])

                remainingSkills.remove(bestSkill)
                candidates.append((bestPerson, bestSkill))

            if not remainingSkills:
                maxCompletionTime = 0
                for tup in candidates:
                    person = tup[0]
                    skill = tup[1]

                    person.time += project.duration
                    maxCompletionTime = max(maxCompletionTime, person.time)
                    # project.complete = True
                    # TODO inequality performance fix
                    if person.skills[skill] == project.skills[skill] - 1 or person.skills[skill] == project.skills[skill]:
                        person.skills[skill] += 1

                    project.persons.append((person, skill))
                    self.planned_projects.append(project)

        print("GREEDY")

    def improve(self):
        print("IMPROVE")