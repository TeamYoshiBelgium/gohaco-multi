class Request:
    CNTR = 0

    def __init__(self, Optimizer, video, endpoint, count):
        self.O = Optimizer
        self.No = Request.CNTR

        self.video = video
        self.endpoint = endpoint
        self.count = count

        Request.CNTR += 1

        self.endpoint.addRequest(self)

        self.saved = 0


    def __gt__(self, other):
        return self.No > other.No

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "REQ%03s()" % (self.No)

