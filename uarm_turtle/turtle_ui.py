from PyQt5 import QtWidgets, QtCore, QtGui

from uarm_turtle.turtle import Turtle
from uarm_turtle.mapper import Map


class TurtleWidget(QtWidgets.QWidget, Turtle):

    def __init__(self, parent):
        super(TurtleWidget, self).__init__()
        self.init_ui()


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
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, 0, width, 0)
        qp.drawLine(0, 0, 0, height)
        qp.drawLine(width, height, width, 0)
        qp.drawLine(width, height, 0, height)


    def run_code(turtle, code):
        turtle.reset()
        exec(code)
        print("Running: ", code)
        print(turtle.log)
        map = Map(turtle.log)
        map.unit_vector()
