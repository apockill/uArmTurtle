from time import sleep

from PyQt5 import QtWidgets, QtCore, QtGui

from uarm_turtle.turtle import Turtle
from uarm_turtle.mapper import Map


class TurtleWidget(QtWidgets.QWidget):
    BACKGROUND_COLOR = (255, 255, 255)
    PEN_COLOR = QtCore.Qt.black
    FPS = 30

    def __init__(self, parent):
        super().__init__(parent)
        self.turtle = Turtle()
        self.init_ui()

        # Handle the animation of the turtle vectors
        self.animation = []  # A list of all line vectors drawn by the turtle
        self.cur_frame = 0  # The current frame that the animation is on
        self.animation_timer = QtCore.QTimer()  # Needs to exist so that singleshots don't get garbage collected
        self.animation_timer.timeout.connect(self.animate)
        self.animation_timer.start(1000.0 / self.FPS)

    def init_ui(self):
        self.setMinimumHeight(500)
        self.setMinimumWidth(500)
        self.show()

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def draw(self, qp):
        """ In this event all lines get drawn"""
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        qp.setPen(QtGui.QPen(QtCore.Qt.lightGray, 2, QtCore.Qt.SolidLine))
        qp.setBrush(QtGui.QColor(*self.BACKGROUND_COLOR))
        qp.drawRect(0, 0, width, height)

        pen = QtGui.QPen(self.PEN_COLOR, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        # Draw current animation frames
        for line in self.animation[:self.cur_frame]:
            qp.drawLine(line[0][0], line[0][1], line[1][0], line[1][1])


    def reset_canvas(self):
        self.animation = []
        self.cur_frame = 0

        self.animation = []
        self.update()

    def animate(self):
        """
        Animate the drawing of the vectors in the map, one by one, calling a singleshot timer each time to
        continue the animation
        :param [[x,y], [x,y], [x, y], [x, y]]:
        :return:
        """
        self.cur_frame = self.cur_frame + 1 if self.cur_frame < len(self.animation) else len(self.animation)
        self.update()

    def run_code(self, code):
        """ Returns None if it was unable to parse the code or the map was invalid (only one move)"""

        turtle = self.turtle
        turtle.reset()
        exec(code)
        # try:
        #     exec(code)
        # except Exception as e:
        #     print("ERROR!", e)
        #     self.reset_canvas()
        #     return None

        # Reset the canvas
        self.reset_canvas()

        # Check if the user actually changed anything
        if len(turtle.map) == 1:
            return None

        map = Map(turtle.map)
        bounds = (0, 0, self.frameGeometry().width(), self.frameGeometry().height())
        bounded = map.fit_to(bounds)
        self.animation = bounded.to_int().get_lines()
        self.cur_frame = 0

        return bounded.unit_vector()
