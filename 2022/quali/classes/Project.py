class Project:

    def __init__(self, name, duration, score, before, skills):
        self.name = name
        self.duration = duration
        self.score = score
        self.before = before
        self.skills = skills

        self.complexity = self.get_complexity()
        self.order = self.get_order()


    def __str__(self):
        return "%s: %s %s %s" % (self.name, self.duration, self.score, self.before)

    def __repr__(self):
        return str(self)

    def get_complexity(self):
        complexity = 0
        for (key, value) in self.skills:
            complexity += value

        return complexity

    def get_order(self):
        return self.duration + (1 - (1 / self.complexity))
