class Project:

    def __init__(self, name, duration, score, before, roles):
        self.name = name
        self.duration = duration
        self.score = score
        self.before = before
        self.roles = roles

    def __str__(self):
        return "%s: %s %s %s" % (self.name, self.duration, self.score, self.before)

    def __repr__(self):
        return str(self)
