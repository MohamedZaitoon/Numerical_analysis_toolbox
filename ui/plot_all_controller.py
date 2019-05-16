import traceback

from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from numpy import *

from root_finder_methods.FalsePosition import FalsePosition
from root_finder_methods.GeneralAlgorithm import GeneralAlgorithm
from root_finder_methods.abstract_method import Method
from root_finder_methods.bierge_vieta import BiergeVieta
from root_finder_methods.bisection import Bisection
from root_finder_methods.fixed_point import FixedPoint
from root_finder_methods.newtonRaphson import NewtonRaphson
from root_finder_methods.secant import Secant
from ui.plotting_main import Ui_MainWindow


class AllMethodsPlot(QMainWindow, Ui_MainWindow):

    def __init__(self, equation, x1, x2, current_absolute, current_iterations):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.equation = equation
        self.x1 = x1
        self.x2 = x2
        self.current_absolute = current_absolute
        self.current_iterations = current_iterations
        self.iteration_counter = 0
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.plotting_area.canvas, self))
        self.plot_tools.setLayout(layout)

        self.bisection = Bisection(self.equation, x1, x2)
        self.secant = Secant(self.equation, x1, x2)
        self.birege = BiergeVieta(self.equation, x1)
        self.fixed = FixedPoint(self.equation, x1)
        self.newton = NewtonRaphson(self.equation, x1)
        self.falseposion = FalsePosition(self.equation, x1, x2)
        self.general = GeneralAlgorithm(self.equation)
        self.method = None

        self.evaluate_method(self.bisection)
        self.evaluate_method(self.secant)
        self.evaluate_method(self.birege)
        self.evaluate_method(self.fixed)
        self.evaluate_method(self.newton)
        self.evaluate_method(self.falseposion)
        self.evaluate_method(self.general)

        self.next_step_button.clicked.connect(self.next_step)
        self.previous_step_button.clicked.connect(self.previous_step)
        self.plot_method_button.clicked.connect(self.plot)

    def evaluate_method(self, method: Method):
        try:
            method.evaluate()
        except Exception:
            pass

    def plot(self):
        self.iteration.setText("")
        self.current_root.setText("")
        current_method = str(self.plot_method.currentText())
        self.method = None
        if current_method == "Bisection":
            self.method = self.bisection
        elif current_method == "Secant":
            self.method = self.secant
        elif current_method == "Bierge-Vieta":
            self.method = self.birege
        elif current_method == "Fixed Point":
            self.method = self.fixed
        elif current_method == "Newton-Raphson":
            self.method = self.newton
        elif current_method == "False Position":
            self.method = self.falseposion
        elif current_method == "General Algorithm":
            self.method = self.general
        elif current_method == "Iterations  Root":
            self.plot_it_roots()
        elif current_method == "Iterations  Error":
            self.plot_it_error()
        if self.method is not None:
            try:
                if self.method.get_error():
                    self.current_root.setText("Error")
                    return
                self.method.plot(self.plotting_area.canvas)
            except Exception:
                self.current_root.setText("Error ")
                print(Exception)
                traceback.print_exc()

    def plot_it_roots(self):
        bir = self.bisection.get_roots()
        secr = self.secant.get_roots()
        flsr = self.falseposion.get_roots()
        fxr = self.fixed.get_roots()
        birgr = self.birege.get_roots()
        newr = self.newton.get_roots()
        genr = self.general.get_roots()

        self.plotting_area.canvas.axes.clear()
        if len(bir) != 0:
            biit = self.iterations_array(len(bir))
            self.plotting_area.canvas.axes.plot(list(biit), list(bir), label="Bisection")
        if len(secr) != 0:
            secit = self.iterations_array(len(secr))
            self.plotting_area.canvas.axes.plot(secit, secr, label="Secant")
        if len(flsr) != 0:
            flsit = self.iterations_array(len(flsr))
            self.plotting_area.canvas.axes.plot(flsit, flsr, label="False position")
        if len(fxr) != 0:
            fxit = self.iterations_array(len(fxr))
            self.plotting_area.canvas.axes.plot(fxit, fxr, label="Fixed point")
        if len(birgr) != 0:
            birgit = self.iterations_array(len(birgr))
            self.plotting_area.canvas.axes.plot(birgit, birgr, label="Bierge vieta")
        if len(newr) != 0:
            newit = self.iterations_array(len(newr))
            self.plotting_area.canvas.axes.plot(newit, newr, label="Newton-Raphson")
        if len(genr) != 0:
            genit = self.iterations_array(len(genr))
            self.plotting_area.canvas.axes.plot(genit, genit, label="General Algorithm")
        self.plotting_area.canvas.axes.set_xlim(self.x1-2, self.x2+2)
        self.plotting_area.canvas.axes.axvline(0)
        self.plotting_area.canvas.axes.axhline(0)
        self.plotting_area.canvas.axes.legend()
        self.plotting_area.canvas.show()

    def plot_array(self, x, y, lab):
        self.plotting_area.canvas.axes.plot(x, y, label=lab)

    def iterations_array(self, s: int):
        l =[]
        for i in range (s):
            l.append(i)
        return l

    def plot_it_error(self):
        bir = self.bisection.get_errors()
        secr = self.secant.get_errors()
        flsr = self.falseposion.get_errors()
        fxr = self.fixed.get_errors()
        birgr = self.birege.get_errors()
        newr = self.newton.get_errors()
        genr = self.general.get_errors()

        self.plotting_area.canvas.axes.clear()
        if len(bir) != 0:
            biit = self.iterations_array(len(bir))
            self.plotting_area.canvas.axes.plot(list(biit), list(bir), label="Bisection")
        if len(secr) != 0:
            secit = self.iterations_array(len(secr))
            self.plotting_area.canvas.axes.plot(secit, secr, label="Secant")
        if len(flsr) != 0:
            flsit = self.iterations_array(len(flsr))
            self.plotting_area.canvas.axes.plot(flsit, flsr, label="False position")
        if len(fxr) != 0:
            fxit = self.iterations_array(len(fxr))
            self.plotting_area.canvas.axes.plot(fxit, fxr, label="Fixed point")
        if len(birgr) != 0:
            birgit = self.iterations_array(len(birgr))
            self.plotting_area.canvas.axes.plot(birgit, birgr, label="Bierge vieta")
        if len(newr) != 0:
            newit = self.iterations_array(len(newr))
            self.plotting_area.canvas.axes.plot(newit, newr, label="Newton-Raphson")
        if len(genr) != 0:
            genit = self.iterations_array(len(genr))
            self.plotting_area.canvas.axes.plot(genit, genit, label="General Algorithm")
        self.plotting_area.canvas.axes.axvline(0)
        self.plotting_area.canvas.axes.axhline(0)
        self.plotting_area.canvas.axes.set_xlim(self.x1 - 2, self.x2 + 2)
        self.plotting_area.canvas.axes.legend()
        self.plotting_area.canvas.show()

    def next_step(self):
        if self.method is None:
            self.current_root.setText("Error")
            return
        if self.iteration_counter < self.method.get_iterations() - 1:
            current_step = self.method.next_step()
            self.iteration_counter += 1
            self.current_root.setText(str(self.method.get_root_value()))
            self.iteration.setText(str(self.iteration_counter))

    def previous_step(self):
        if self.method is None:
            self.current_root.setText("Error")
            return
        if self.iteration_counter > 0:
            current_step = self.method.prev_step()
            self.iteration_counter -= 1
            self.current_root.setText(str(self.method.get_root_value()))
            self.iteration.setText(str(self.iteration_counter))
