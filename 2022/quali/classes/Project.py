class Project:

    def __init__(self, name, duration, score, before):
        self.name = name
        self.duration = duration
        self.score = score
        self.before = before
        self.roles = dict()

    def __str__(self):
        return "%s" % self.name
