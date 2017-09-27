import ast

from PyQt5 import QtWidgets, QtGui


class LineTextWidget(QtWidgets.QFrame):
    """
    This puts line numbers on a QTextEdit widget
    """

    class NumberBar(QtWidgets.QWidget):

        def __init__(self, *args):
            QtWidgets.QWidget.__init__(self, *args)
            self.edit = None
            # This is used to update the width of the control.
            # It is the highest line that is currently visibile.
            self.highest_line = 0

        def setTextEdit(self, edit):
            self.edit = edit

        def update(self, *args):
            """
            Updates the number bar to display the current set of numbers.
            Also, adjusts the width of the number bar if necessary.
            """

            # The + 4 is used to compensate for the current line being bold.
            width = self.fontMetrics().width(str(self.highest_line)) + 4
            if self.width() != width:
                self.setFixedWidth(width)
            QtWidgets.QWidget.update(self, *args)

        def paintEvent(self, event):

            contents_y = self.edit.verticalScrollBar().value()
            page_bottom = contents_y + self.edit.viewport().height()
            font_metrics = self.fontMetrics()
            current_block = self.edit.document().findBlock(self.edit.textCursor().position())

            painter = QtGui.QPainter(self)

            line_count = 0
            # Iterate over all text blocks in the document.
            block = self.edit.document().begin()
            while block.isValid():
                line_count += 1

                # The top left position of the block in the document
                position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

                # Check if the position of the block is out side of the visible
                # area.
                if position.y() > page_bottom:
                    break

                # We want the line number for the selected line to be bold.
                bold = False
                if block == current_block:
                    bold = True
                    font = painter.font()
                    font.setBold(True)
                    painter.setFont(font)

                # Draw the line number right justified at the y position of the
                # line. 3 is a magic padding number. drawText(x, y, text).
                painter.drawText(self.width() - font_metrics.width(str(line_count)) - 3,
                                 round(position.y()) - contents_y + font_metrics.ascent(),
                                 str(line_count))

                # Remove the bold style if it was set previously.
                if bold:
                    font = painter.font()
                    font.setBold(False)
                    painter.setFont(font)

                block = block.next()

            self.highest_line = line_count
            painter.end()

            QtWidgets.QWidget.paintEvent(self, event)

    def __init__(self, *args):
        QtWidgets.QFrame.__init__(self, *args)

        self.setFrameStyle(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Sunken)

        self.edit = QtWidgets.QTextEdit()
        self.edit.setFrameStyle(QtWidgets.QFrame.NoFrame)
        self.edit.setAcceptRichText(False)
        self.edit.setTabStopWidth(28)

        self.number_bar = self.NumberBar()
        self.number_bar.setTextEdit(self.edit)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.setSpacing(0)
        # hbox.setMargin(0)
        hbox.addWidget(self.number_bar)
        hbox.addWidget(self.edit)

        self.edit.installEventFilter(self)
        self.edit.viewport().installEventFilter(self)

    # noinspection PyArgumentList
    def eventFilter(self, obj, event):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if obj in (self.edit, self.edit.viewport()):
            self.number_bar.update()
            return False
        return QtWidgets.QFrame.eventFilter(obj, event)

    def setText(self, plainText):
        self.edit.setPlainText(plainText)

    def getTextEdit(self):
        return self.edit

    def getText(self):
        return self.edit.toPlainText()


class ScriptWidget(QtWidgets.QWidget):
    """This class is for making a text editor that will help you write python code"""

    def __init__(self, parent):
        super(ScriptWidget, self).__init__(parent)

        self.text_edit = LineTextWidget()

        self.hint_lbl = QtWidgets.QLabel("")  # Will give you warnings and whatnot
        self.init_ui()

    def init_ui(self):

        bold = QtGui.QFont()
        bold.setBold(True)
        self.hint_lbl.setFont(bold)

        monospace = QtGui.QFont("Monospace")
        monospace.setStyleHint(QtGui.QFont.TypeWriter)
        self.text_edit.setFont(monospace)
        self.setMinimumHeight(500)
        self.setMinimumWidth(350)
        self.setMaximumWidth(700)
        self.text_edit.getTextEdit().textChanged.connect(self.verify_code)

        row1 = QtWidgets.QHBoxLayout()
        row2 = QtWidgets.QHBoxLayout()
        row3 = QtWidgets.QHBoxLayout()

        row1.addStretch(1)

        row2.addWidget(self.text_edit)
        row3.addWidget(self.hint_lbl)

        mainVLayout = QtWidgets.QVBoxLayout()
        mainVLayout.addLayout(row1)
        mainVLayout.addLayout(row2)
        mainVLayout.addLayout(row3)

        self.setLayout(mainVLayout)

    def get_code(self):
        return self.text_edit.getText()

    def verify_code(self):
        # Checks if the users code is valid, and updates self.applyBtn
        code = self.text_edit.getText()

        error = ""

        try:
            ast.parse(code)
        except SyntaxError as e:
            error = str(e)

        self.hint_lbl.setText(error)

    def set_code(self, code):
        self.text_edit.setText(code)