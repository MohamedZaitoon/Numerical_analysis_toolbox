from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from methods.methodDemo import Demo
from ui.gui_demo import Ui_MainWindow
import sys
from methods.Newton_Raphson import NewtonRaphson
from matplotlib.backends.qt_compat import is_pyqt5

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
        self.m = NewtonRaphson()
        self.setupUi(self)
        layout = QVBoxLayout(self.plot)
        self.static_canvas = FigureCanvas(Figure(figsize=(10, 5)))
        layout.addWidget(self.static_canvas)
        layout.addWidget(NavigationToolbar(self.static_canvas, self))
        self.graph = self.static_canvas.figure.subplots()
        self.select.clicked.connect(self.evaluate)
        self.nextButton.clicked.connect(self.next)
        self.prevButton.clicked.connect(self.prev)
        self.saveButton.clicked.connect(self.save)
        self.equation.setText('write the equation here!')

    @pyqtSlot()
    def next(self):
        self.graph.clear()
        self.m.next_step(self.graph)
        self.graph.figure.canvas.draw()
        print("plot next success")

    @pyqtSlot()
    def prev(self):
        self.graph.clear()
        self.m.prev_step(self.graph)
        self.graph.figure.canvas.draw()
        print("plot prev success")

    @pyqtSlot()
    def save(self):
        self.m.output_file()

    @pyqtSlot()
    def evaluate(self):
        selected = self.methods.currentText()

        if selected == 'Bisection':
            self.graph.clear()
            m = Demo()
            eq = str(self.equation.text())
            m.calculate(eq)
            m.plot(self.graph)
            self.graph.figure.canvas.draw()
            print("evaluate")
        elif selected == 'Newton-Raphson':
            self.graph.clear()
            eq = str(self.equation.text())
            self.m.calculate(eq, 3)
            self.m.plot(self.graph)
            self.graph.figure.canvas.draw()
            print("evaluate")
        else:
            self.graph.clear()
            self.graph.figure.canvas.draw()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
