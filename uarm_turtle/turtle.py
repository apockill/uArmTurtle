from math import sin, cos, radians

from uarm_turtle.mapper import Map


class Turtle:
    """
    The turtle initially faces right
    """

    def __init__(self):
        self.pos = None
        self.dir = None
        self.pen_down = False  # True: Pen down, False: Pen up
        self.map = Map()

        self.reset()


    def __repr__(self):
        return str(self.pos) + " " + str(self.dir)

    def reset(self):
        self.pos = [0, 0]
        self.dir = 0
        self.pen_down = False

        self.map = Map()
        self.map.append(self.pos, self.pen_down)

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

    def pen_up(self):
        self.pen_down = False
        self.postprocess()

    def pen_down(self):
        self.pen_down = True
        self.postprocess()

    @property
    def position(self):
        return self.pos

    @property
    def heading(self):
        return self.dir


    def postprocess(self):
        self.map.append(self.pos, self.pen_down)