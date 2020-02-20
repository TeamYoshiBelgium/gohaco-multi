import math

class Writer:
    def __init__(self, L):
        self.L = L

    def write(self):
        score = 0
        actions = []
        for order in self.L.O.orders:
            if (order.finished):
                score += math.ceil((self.L.turns - order.finishTime)/self.L.turns * 100)

        for drone in self.L.O.drones:
            actions += drone.actions

        filename = self.L.filename.replace(".in", "." + str(score) + ".out").replace("in/", "out/")

        with open(filename, 'w+') as file:
            file.write(str(len(actions)) + '\n')

            for action in actions:
                file.write(action.toString() + '\n')

        print(self.L.filename, "=>", filename)

        print("SCORE:", score)
