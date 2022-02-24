class Person:
    _No = 0

    def __init__(self, name, skills):
        self.name = name
        self.time = 0
        self.skills = skills

        self.No = Person._No
        Person._No += 1


    def __str__(self):
        return "PERSON[%s]" % (self.name)

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        if self.time < other.time:
            return True
        
        if self.time == other.time:
            return self.No < other.No

        return False