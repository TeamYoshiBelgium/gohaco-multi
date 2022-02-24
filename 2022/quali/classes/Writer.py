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
        score = 0

        # score = calc_score()

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
            file.write(str(len(self.E.O.planned_projects)))
            file.write("\n")
            for project in self.E.O.planned_projects:
                file.write(project.name)
                file.write("\n")
                for people in project.peoples:
                    file.write(people.name)
                    file.write("\n")
            pass
            


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