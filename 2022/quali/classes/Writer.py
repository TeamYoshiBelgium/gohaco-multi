from classes import Engine, Loader
from .Settings import Settings

def right_pad(string, length):
    string = string[:length-2]

    return string + " " * (length - len(string))

class Writer:
    def __init__(self, L: Loader, E: Engine):
        self.L = L
        self.E = E

    def write(self):
        score = self.calc_score()

        if score == 0:
            return

        # in/a.txt
        # out/a.0000001411102.v0.1[0.5__1.3__9.2].out
        outFile = self.L.filename.replace(
            ".txt", (
                "." + ("%012d" % score) + 
                "." + "v" + str(Settings.version) + 
                "[" + "__".join(map(str, self.L.get_heuristic())) + "]" + 
                ".out"
            )
        ).replace("in/", "out/")

        self.print_footer(score, outFile)

        with open(outFile, 'w+') as file:
            file.write(str(len(self.E.planned_projects)))
            file.write("\n")
            for project in self.E.planned_projects:
                file.write(project.name)
                file.write("\n")
                for person in project.persons:
                    file.write(person.name)
                    file.write(" ")
                file.write("\n")
            pass
            
    def calc_score(self):
        score = 0
        for project in self.E.planned_projects:
            days_late = project.before - project.completion_date
            if days_late >= 0:
                score += project.score
            elif days_late < project.score:
                score += max(0, project.score + days_late)
        return score


    def print_footer(self, score, outFile):
        width = Settings.width

        print()
        print("-" * width)
        print(right_pad("[ Input File:   %s" % self.L.filename,       width-1) + "]")
        print(right_pad("[ Heuristics:   %s" % str(self.L.heuristic), width-1) + "]")
        print("-" * width)
        print(right_pad("[ Output File:  %s" % outFile,               width-1) + "]")
        print(right_pad("[ Score:        %d" % score,                 width-1) + "]")
        print("-" * width)
        print()