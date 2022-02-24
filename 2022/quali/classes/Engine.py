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

        finishedProjects = set()

        pointer = 0
        iterations = 0

        while True:

            if iterations%10 == 0:
                print(len(finishedProjects), "/", len(self.projects), " (", pointer, ")", flush=True)

            iterations += 1

            candidateProjects = []

            for project in projects:
                # if pointer >= len(self.projects):
                #     break



                # print(len(projects))

                # project = projects[pointer]
                if project in finishedProjects:
                    pointer += 1
                    continue

                # for skill in project.skills:
                candidates = []
                usedPersons = set()

                remainingSkills = []
                index = 0
                for tup in project.skills:
                    remainingSkills.append((tup[0], tup[1], index))
                    index += 1


                skillMentorLevels = {}

                while remainingSkills:
                    personScores = []

                    for person in self.persons:
                        if person in usedPersons:
                            continue

                        if (person.time + project.duration) > project.before + project.score:
                            continue

                        score = 0
                        for tup in remainingSkills:
                            # print(skill, project.skills[skill], person.skills, skill in person.skills)
                            skill = tup[0]
                            level = tup[1]
                            skillIndex = tup[2]

                            if skill in person.skills:
                                if level < person.skills[skill]:
                                    score += 1
                                # Learning yourself
                                elif level == person.skills[skill]:
                                    score += 2
                                # Learning by being mentored
                                elif level - 1 == person.skills[skill] and skill in skillMentorLevels and skillMentorLevels[skill] >= level:
                                    score += 2.5

                        # TODO Correction: maximum possible score remaining instead of project score
                        timeFactor = (project.score - min(0, project.before - (person.time + project.duration)))/project.score

                        if score == 0:
                            continue

                        heapq.heappush(personScores, (-score * timeFactor, person))

                    # We cannot complete this project at this time
                    # print(project)
                    if not personScores:
                        # print("CANNOT COMPLETE PROJECT")
                        # TODO: re-add, but find termination conditions?
                        # projects.append(project)
                        pointer += 1
                        break

                    # print(personScores)

                    bestPerson = heapq.heappop(personScores)[1]
                    bestSkill = None
                    bestSkillIndex = -1

                    # print("PRSN",bestPerson.skills)
                    # print("PROJ",project.skills)
                    # print("REMAINING",remainingSkills)
                    for tup in sorted(remainingSkills, key=lambda tup: tup[1], reverse=True):
                        skill = tup[0]
                        level = tup[1]
                        skillIndex = tup[2]

                        # print(skill, skill in bestPerson.skills)
                        if skill not in bestPerson.skills:
                            continue

                        qualified = (level <= bestPerson.skills[skill])
                        mentored = (level - 1 == bestPerson.skills[skill] and skill in skillMentorLevels and skillMentorLevels[skill] >= level)
                        # print(skill, qualified, mentored)
                        if qualified or mentored:
                            bestSkill = skill
                            bestSkillIndex = skillIndex
                            break

                    for skill in bestPerson.skills:
                        skillLevel = 0
                        if skill in skillMentorLevels:
                            skillLevel = skillMentorLevels[skill]

                        skillMentorLevels[skill] = max(skillLevel, bestPerson.skills[skill])

                    index = 0
                    for tup in remainingSkills:
                        if bestSkillIndex == tup[2]:
                            del remainingSkills[index]
                            break
                        index += 1

                    candidates.append((bestPerson, bestSkill, bestSkillIndex))
                    usedPersons.add(bestPerson)

                if not remainingSkills:

                    maxCompletionTime = 0
                    for tup in candidates:
                        person = tup[0]
                        skill = tup[1]
                        skillIndex = tup[2]

                        maxCompletionTime = max(maxCompletionTime, person.time+project.duration)

                    if maxCompletionTime > project.before + project.score:
                        continue

                    timePenalty = 0
                    if maxCompletionTime < project.before:
                        timePenalty = (project.before - maxCompletionTime)/project.before
                    elif maxCompletionTime > project.before:
                        timePenalty = (maxCompletionTime - project.before)/project.score

                    complexityPenalty = 1-1/project.complexity

                    score = timePenalty + complexityPenalty

                    heapq.heappush(candidateProjects, (score, project, candidates))
                    # maxCompletionTime = 0
                    # for tup in candidates:
                    #     person = tup[0]
                    #     skill = tup[1]
                    #     skillIndex = tup[2]

                    #     person.time += project.duration
                    #     maxCompletionTime = max(maxCompletionTime, person.time)
                    #     # project.complete = True
                    #     # TODO inequality performance fix
                    #     if person.skills[skill] == project.skills[skillIndex][1] - 1 or person.skills[skill] == project.skills[skillIndex][1]:
                    #         person.skills[skill] += 1

                    #     project.persons[skillIndex] = person

                    # for tup in candidates:
                    #     person.time = maxCompletionTime

                    # # project.persons = sorted(project.persons, key=lambda tup: tup[1])
                    # self.planned_projects.append(project)
                    # finishedProjects.add(project)

                    # project.completion_date = maxCompletionTime
                    # pointer = 0

            if not candidateProjects:
                break
            else:
                bestProject = heapq.heappop(candidateProjects)
                print(bestProject)

                candidates = bestProject[2]
                project = bestProject[1]

                maxCompletionTime = 0
                for tup in candidates:
                    person = tup[0]
                    skill = tup[1]
                    skillIndex = tup[2]

                    person.time += project.duration
                    maxCompletionTime = max(maxCompletionTime, person.time)
                    # project.complete = True
                    # TODO inequality performance fix
                    if person.skills[skill] == project.skills[skillIndex][1] - 1 or person.skills[skill] == project.skills[skillIndex][1]:
                        person.skills[skill] += 1

                    project.persons[skillIndex] = person

                for tup in candidates:
                    person.time = maxCompletionTime

                # project.persons = sorted(project.persons, key=lambda tup: tup[1])
                self.planned_projects.append(project)
                finishedProjects.add(project)

                project.completion_date = maxCompletionTime

    def improve(self):
        print("IMPROVE")