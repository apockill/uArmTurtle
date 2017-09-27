from math import sin, cos, radians



class Turtle:
    """
    The turtle initially faces right
    """

    def __init__(self):
        self.pos = (0, 0)
        self.dir = 0

        # A log of coordinates
        self.log = []


    def __repr__(self):
        return str(self.pos) + " " + str(self.dir)

    def reset(self):
        self.pos = (0, 0)
        self.dir = 0
        self.log = []

    def forward(self, unit):
        new_x = unit * cos(radians(self.dir)) + self.pos[0]
        new_y = unit * sin(radians(self.dir)) + self.pos[1]
        self.pos = (new_x, new_y)
        self.postprocess()

    def backward(self, unit):
        self.forward(-unit)

    def right(self, degrees):
        self.dir = self.dir + degrees
        self.postprocess()

    def left(self, degrees):
        self.right(-degrees)


    @property
    def position(self):
        return self.pos

    @property
    def heading(self):
        return self.dir


    def postprocess(self):
        print(self)
        self.log.append([self.pos, self.dir])