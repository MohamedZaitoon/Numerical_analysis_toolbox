from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.gui_demo import Ui_MainWindow
import sys
import time
from methods.methodDemo import Demo

import numpy as np

from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5

if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        layout = QVBoxLayout(self.plot)
        self.static_canvas = FigureCanvas(Figure(figsize=(10, 5)))
        layout.addWidget(self.static_canvas)
        layout.addWidget(NavigationToolbar(self.static_canvas, self))
        self.graph = self.static_canvas.figure.subplots()
        self.select.clicked.connect(self.evaluate)


    @pyqtSlot()
    def evaluate(self):
        selected = self.methods.currentText()
        if selected == 'Bisection':
            self.graph.clear()
            m = Demo()
            m.calculate(self.equation.text())
            m.plot(self.graph)
            self.graph.figure.canvas.draw()
            print("evaluate")
        else:
            pass
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
