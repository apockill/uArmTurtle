import sys

from PyQt5 import QtWidgets, QtGui

import paths
from robot_mapper import RobotMapper
from code_editor import ScriptWidget
from uarm_turtle.turtle_ui import TurtleWidget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, dev_port):
        super().__init__()
        self.robot_running = False
        self.current_map = None

        self.robot_mapper = RobotMapper(dev_port)
        self.script = ScriptWidget(self)
        self.turtle = TurtleWidget(self)

        # Global UI Elements
        self.run_robot_action = QtWidgets.QAction(QtGui.QIcon(paths.robot_run), "Play", self)

        self.init_ui()


    def init_ui(self):
        toggle_robot = lambda: self.stop_robot() if self.robot_running else self.run_robot()

        # Set up menubar actions
        save_action = QtWidgets.QAction(QtGui.QIcon(paths.file_save_icon), 'Save', self)
        load_action = QtWidgets.QAction(QtGui.QIcon(paths.file_load_icon), 'Load', self)
        new_action = QtWidgets.QAction(QtGui.QIcon(paths.file_new_icon), 'New Project', self)
        run_script_action = QtWidgets.QAction(QtGui.QIcon(paths.script_run), "Evaluate", self)


        load_action.triggered.connect(self.load)
        new_action.triggered.connect(self.new)
        save_action.triggered.connect(self.save)
        run_script_action.triggered.connect(self.run_script)
        self.run_robot_action.triggered.connect(toggle_robot)

        run_script_action.setShortcut('Ctrl+R')

        # Set up MenuBar
        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(new_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

        # Set up ToolBar
        toolbar = self.addToolBar('Run')
        toolbar.addAction(run_script_action)
        toolbar.addAction(self.run_robot_action)

        # Put a GBox around the turtle widget
        turtle_layout = QtWidgets.QHBoxLayout()
        turtle_layout.addWidget(self.turtle)
        turtle_gbox = QtWidgets.QGroupBox("Turtle")
        turtle_gbox.setLayout(turtle_layout)


        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(self.script)
        main_layout.addWidget(turtle_gbox)
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
        test = "turtle.forward(10)\nturtle.right(90)\nturtle.backward(15)\nturtle.left(20)\nturtle.forward(5)"
        test = "turtle.forward(10)\nturtle.right(60)\n" * 6
        output_map = self.turtle.run_code(test)
        self.current_map = output_map

    def run_robot(self):
        if self.current_map is None: return
        self.robot_running = True
        self.run_robot_action.setIcon(QtGui.QIcon(paths.robot_stop))
        self.robot_mapper.draw_map(self.current_map)

    def stop_robot(self):
        self.robot_running = False
        self.run_robot_action.setIcon(QtGui.QIcon(paths.robot_run))
        self.robot_mapper.stop()

    def closeEvent(self, event):
        self.robot_mapper.stop()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow("/dev/ttyACM0")
    sys.exit(app.exec_())