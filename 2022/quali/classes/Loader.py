import os

from .Engine import Engine
from .Settings import Settings
from .Person import Person
from .Project import Project


def read_int_array(file):
    return list(map(int, read_array(file)))

def read_array(file):
    return file.readline().strip().split(" ")

def right_pad(string, length):
    string = string[:length-2]

    return string + " " * (length - len(string))

def get_filename_no_extension(filepath):
    filename = os.path.split(filepath)[1]
    
    return os.path.splitext(filename)[0]

class Loader:
    def __init__(self, filename): 
        self.filename = filename
        self.heuristic = self.get_heuristic()

        with open(filename) as file:
            # Usually first line is a parameter line
            self.params = read_int_array(file)

            self.personCount = params[0]
            self.projectCount = params[1]

            self.persons = []
            self.read_persons(file)

            self.projects = []
            self.read_projects(file)

            self.engine = Engine(self.heuristic, self.projects, self.persons)

            self.print_header()

            # read rest of file, read_array, read_int_array and stuff

    def read_persons(self, file):
        for i in range(self.personCount):
            line = read_array(file)
            name = line[0]
            skillCount = int(line[1])

            skills = {}
            for j in range(skillCount):
                line2 = read_array(file)
                skillName = line2[0]
                level = int(line2[1])

                if skillName in skills:
                    raise "Duplicate skill"

                skills[skillName] = level

            person = Person(name, skills)
            self.persons.append(person)


    def read_projects(self, file):
        for i in range(self.projectCount):
            line = read_array(file)
            name = line[0]
            days = int(line[1])
            score = int(line[2])
            before = int(line[3])
            roleCount = int(line[4])

            skills = {}
            for j in range(roleCount):
                line2 = read_array(file)
                skillName = line2[0]
                level = int(line2[1])

                if skillName in skills:
                    raise "Duplicate skill"

                skills[skillName] = level

            project = Project(name, days, score, before, skills)

            self.projects.append(project)

    def get_heuristic(self):
        realFile = get_filename_no_extension(self.filename)

        return Settings.heuristics[realFile]

    def print_header(self):
        width = Settings.width
        print("-" * width)
        print(right_pad("[ Version:      %s" % Settings.version,                 width-1) + "]")
        print(right_pad("[ Heuristics:   %s" % str(self.heuristic),              width-1) + "]")
        print("-" * width)
        print(right_pad("[ File:         %s" % self.filename,                    width-1) + "]")
        print(right_pad("[ File Params:  %s" % self.params, width-1) + "]")
        print("-" * width)
        print()
        