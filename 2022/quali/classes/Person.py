class Person:
    def __init__(self, name, skills):
        self.name = name
        self.time = 0
        self.skills = skills
    def __str__(self):
        return "%s" % (self.name)

    def __repr__(self):
        return str(self)

