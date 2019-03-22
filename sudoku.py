import numpy as np
import sys
from datetime import datetime
from functools import partial
from PyQt5.QtWidgets import (QMainWindow, QApplication, QPushButton, QLineEdit,
                             QErrorMessage, QDesktopWidget, QLabel)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSlot, Qt
from solver import solve_sudoku

COLOR_A = '#0FC'
COLOR_B = '#CF6'
COLOR_ERR = '#F00'
COLOR_SOLVED = '#F03'


def use_color_A(i, j):
    return (i // 3 + j // 3) % 2 == 1


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Sudoku Solver'
        self.width = 400
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)

        # centering the window
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        # Create textbox
        for i in range(9):
            for j in range(9):
                # create a QLineEdit
                setattr(self, 'textbox%d%d' % (i, j), QLineEdit(self))
                getattr(self, 'textbox%d%d' % (i, j)).move(
                    20 + 40 * j, 20 + 40 * i)
                getattr(self, 'textbox%d%d' % (i, j)).resize(40, 40)
                getattr(self,
                        'textbox%d%d' % (i, j)).setAlignment(Qt.AlignCenter)
                font = QFont()
                font.setFamily("Comic Sans MS")
                font.setPointSize(16)
                getattr(self, 'textbox%d%d' % (i, j)).setFont(font)
                getattr(self, 'textbox%d%d' % (i, j)).textChanged.connect(
                    partial(self.on_change, i, j, use_color_A(i, j)))

                if use_color_A(i, j):
                    getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                        'background-color: %s;' % COLOR_A)
                else:
                    getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                        'background-color: %s;' % COLOR_B)

        # create the solve button
        self.solve_button = QPushButton('Solve', self)
        self.solve_button.resize(360, 30)
        self.solve_button.move(20, 385)
        consolas = QFont()
        consolas.setFamily("Consolas")
        consolas.setPointSize(12)
        self.solve_button.setFont(consolas)

        # connect the solve button to function on_solve_click
        self.solve_button.clicked.connect(self.on_solve_click)

        # create the clear button
        self.clear_button = QPushButton('Reset', self)
        self.clear_button.resize(360, 30)
        self.clear_button.move(20, 420)
        self.clear_button.setFont(consolas)

        # connect the clear button to function on_clear_click
        self.clear_button.clicked.connect(self.on_clear_click)

        # create console text
        self.console_text = QLabel('Welcome. Esc to exit', self)
        self.console_text.setFixedWidth(390)
        self.console_text.move(20, 450)
        self.console_text.setFont(consolas)

        self.show()

    @pyqtSlot()
    def on_solve_click(self):
        time_a = datetime.now()
        nums = []
        for i in range(9):
            for j in range(9):
                n = getattr(self, 'textbox%d%d' % (i, j)).text()
                if n == '':
                    n = None
                else:
                    n = int(n)
                nums.append(n)
        A = np.array(nums).reshape(9, 9)
        r = solve_sudoku(A)
        if r is None:
            error_dialog = QErrorMessage(self)
            error_dialog.setWindowTitle('Error')
            error_dialog.showMessage('Cannot solve it! Check your input.')
        else:
            for i in range(9):
                for j in range(9):
                    n = getattr(self, 'textbox%d%d' % (i, j)).text()
                    if n == '':
                        getattr(self, 'textbox%d%d' % (i, j)).setText(
                            str(r[i, j]))
                        getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                            'color: %s; background-color: %s' %
                            (COLOR_SOLVED, [COLOR_B, COLOR_A][use_color_A(
                                i, j)]))
            time_b = datetime.now()
            time_delta = time_b - time_a
            self.console_text.setText(
                'Solved in %s ms' % str(time_delta.microseconds // 1000))

    @pyqtSlot()
    def on_clear_click(self):
        self.console_text.setText('Welcome. Esc to exit')
        for i in range(9):
            for j in range(9):
                getattr(self, 'textbox%d%d' % (i, j)).setText('')
                getattr(self,
                        'textbox%d%d' % (i, j)).setStyleSheet('color: black;')
                if use_color_A(i, j):
                    getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                        'background-color: %s;' % COLOR_A)
                else:
                    getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                        'background-color: %s;' % COLOR_B)

    @pyqtSlot()
    def on_change(self, i, j, is_color_A):
        n = getattr(self, 'textbox%d%d' % (i, j)).text()
        if len(n) == 1 and not n.isdigit() or len(n) > 1:
            getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                'background-color: %s;' % COLOR_ERR)
            self.solve_button.setEnabled(False)
        elif is_color_A:
            getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                'background-color: %s;' % COLOR_A)
            self.solve_button.setEnabled(True)
        else:
            getattr(self, 'textbox%d%d' % (i, j)).setStyleSheet(
                'background-color: %s;' % COLOR_B)
            self.solve_button.setEnabled(True)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    exit_code = App()
    sys.exit(app.exec_())
