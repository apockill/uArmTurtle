import sys

from PyQt5 import QtWidgets, QtGui

import paths
from code_editor import ScriptWidget
from uarm_turtle.turtle_ui import TurtleWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.script = ScriptWidget(self)
        self.turtle = TurtleWidget(self)

        self.init_ui()
        self.turtle.repaint()


    def init_ui(self):

        # Set up menubar actions
        save_action = QtWidgets.QAction(QtGui.QIcon(paths.file_save_icon), 'Save', self)
        load_action = QtWidgets.QAction(QtGui.QIcon(paths.file_load_icon), 'Load', self)
        new_action = QtWidgets.QAction(QtGui.QIcon(paths.file_new_icon), 'New Project', self)
        run_action = QtWidgets.QAction(QtGui.QIcon(paths.script_run), "Run", self)
        load_action.triggered.connect(self.load)
        new_action.triggered.connect(self.new)
        save_action.triggered.connect(self.save)
        run_action.triggered.connect(self.run_script)
        run_action.setShortcut('Ctrl+R')

        # Set up MenuBar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        # Set up ToolBar
        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_action)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.script)
        main_layout.addWidget(self.turtle)
        center_widget = QtWidgets.QWidget()
        center_widget.setLayout(main_layout)

        self.setCentralWidget(center_widget)
        # self.setGeometry(300, 300, 750, 500)
        self.setWindowTitle('uArm Turtle Graphics')
        self.show()

    def new(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

    def run_script(self):
        code = self.script.get_code()
        test = "turtle.forward(10)\nturtle.right(90)\nturtle.backward(15)"
        self.turtle.run_code(test)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())