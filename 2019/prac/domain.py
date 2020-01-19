class Pizza:
    def __init__(self, type, slices):
        self.type = int(type)
        self.slices = int(slices)

    def __str__(self):
        string = "type: %i slices: %i\n" % (self.type, self.slices)
        return string
        
    def __repr__(self):
        string = "type: %i slices: %i" % (self.type, self.slices)
        return string

    def get_score(self):
        return self.slices

class Hub:
    def __init__(self, max_slices, pizzas):
        self.max_slices = int(max_slices)
        self.pizzas = pizzas

    def __str__(self):
        string = "max_slices: %i pizzas: %i\n" % (self.max_slices, len(self.pizzas))
        for pizza in self.pizzas:
            string += str(pizza)
        return string