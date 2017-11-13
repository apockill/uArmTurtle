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
        self.animation_map = []  # A Map objec of the turtle movements
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
        frame_counter = 0
        for cur_pt, next_pt, pen_down in self.animation_map:
            if frame_counter > self.cur_frame: break
            frame_counter += 1

            if not pen_down: continue
            qp.drawLine(cur_pt[0], cur_pt[1], next_pt[0], next_pt[1])


    def reset_canvas(self):
        self.animation_map = []
        self.cur_frame = 0

        self.animation_map = []
        self.update()

    def animate(self):
        """
        Animate the drawing of the vectors in the map, one by one, calling a singleshot timer each time to
        continue the animation
        :param [[x,y], [x,y], [x, y], [x, y]]:
        :return:
        """
        if self.cur_frame < len(self.animation_map):
            self.cur_frame += 1
            self.update()


    def run_code(self, code):
        """ Returns None if it was unable to parse the code or the map was invalid (only one move)"""

        turtle = self.turtle
        turtle.reset()
        print(code)
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
        self.animation_map = bounded
        self.cur_frame = 0

        return bounded.unit_vector()
