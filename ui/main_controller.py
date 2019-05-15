from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from numpy import *
import traceback
from root_finder_methods.FalsePosition import FalsePosition
from root_finder_methods.GeneralAlgorithm import GeneralAlgorithm
from root_finder_methods.bierge_vieta import BiergeVieta
from root_finder_methods.bisection import Bisection
from root_finder_methods.fixed_point import FixedPoint
from root_finder_methods.secant import Secant
from root_finder_methods.newtonRaphson import NewtonRaphson
from ui.keypad import EquationForm
from ui.plot_all_controller import AllMethodsPlot


class MatPlotLibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("main_window.ui", self)
        self.method = None
        self.equation = "sin(x)-x-5"
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.MplWidget.canvas, self))
        self.graph_adjustments.setLayout(layout)
        self.solve_button.clicked.connect(self.solve)
        self.next_step_button.clicked.connect(self.next_step)
        self.previous_step_button.clicked.connect(self.previous_step)
        self.adjust_criteria_button.clicked.connect(self.adjust_criteria)
        self.selected_method.activated.connect(self.adjust_parameters)

        self.dialogs = list()

        self.current_absolute = 0.00001
        self.current_iterations = 50

        self.round_margin = 12
        self.iteration_counter = 0
        self.dialog = EquationForm(self)
        self.edit_function_button.clicked.connect(self.edit_function)

    def solve(self):
        current_method = str(self.selected_method.currentText())
        self.iteration_counter = 0
        current_upper_value = None
        self.clear_components()

        if self.equation is None:
            self.notification.setText("ERROR: Equation is not available")
            return

        if str(self.lower_value_text.text()) == "":
            self.notification.setText("ERROR: Lower Value is not available")
            return
        else:
            try:
                current_lower_value = float(str(self.lower_value_text.text()))
            except ValueError:
                self.notification.setText("ERROR: Lower value error")
                return

        if self.upper_value_text.isEnabled():
            if str(self.upper_value_text.text()) == "":
                self.notification.setText("ERROR: Upper value is not available")
                return
            else:
                try:
                    current_upper_value = float(self.upper_value_text.text())
                except ValueError:
                    self.notification.setText("ERROR: Upper value error")
                    return

        if current_method == "Bisection":
            self.method = Bisection(self.equation, current_lower_value, current_upper_value)
        elif current_method == "Secant":
            self.method = Secant(self.equation, current_lower_value, current_upper_value)
        elif current_method == "Bierge-Vieta":
            self.method = BiergeVieta(self.equation, current_lower_value)
        elif current_method == "Fixed Point":
            self.method = FixedPoint(self.equation, current_lower_value)
        elif current_method == "Newton-Raphson":
            self.method = NewtonRaphson(self.equation, current_lower_value)
        elif current_method == "False Position":
            self.method = FalsePosition(self.equation, current_lower_value, current_upper_value)
        elif current_method == "General Algorithm":
            self.method = GeneralAlgorithm(self.equation)
        elif current_method == "All Methods":
            try:
                newWindow = AllMethodsPlot(self.equation, current_lower_value, current_upper_value,
                                           self.current_absolute,
                                           self.current_iterations)
                self.dialogs.append(newWindow)
                newWindow.show()
            except Exception:
                self.notification.setText("Error ")
                print(Exception)
                traceback.print_exc()
            return

        self.method.set_absolute_error_criteria(self.current_absolute)
        self.method.set_max_iterations_criteria(self.current_iterations)
        try:
            self.method.evaluate()
            if self.method.get_error():
                self.notification.setText("Method Error: Invalid guesses or divergence may occurred")
                return

            self.method.plot(self.MplWidget.canvas)
            self.show_results()
        except Exception:
            self.notification.setText("Error ")
            print(Exception)
            traceback.print_exc()

    def clear_components(self):
        self.notification.setText("")
        self.step_lower_value_text.setText("")
        self.step_upper_value_text.setText("")
        self.step_root_value_text.setText("")
        self.step_absolute_error.setText("")
        self.iteration_couner_text.setText("")
        self.root_value_text.setText("")
        self.iterations_text.setText("")
        self.absolute_error_text.setText("")

    def adjust_parameters(self):
        two_parameter_method = ("Bisection", "Secant", "All Methods", "False Position")
        one_parameter_method = ("Bierge-Vieta", "Fixed Point","Newton-Raphson")
        selected_method = self.selected_method.currentText()
        if two_parameter_method.count(selected_method) != 0:
            self.upper_value_text.setEnabled(True)
        elif one_parameter_method.count(selected_method) != 0:
            self.upper_value_text.setEnabled(False)
            self.upper_value_text.setText("")
        else:
            pass

    def show_results(self):
        self.root_value_text.setText(str(self.method.get_root_value()))
        self.iterations_text.setText(str(self.method.get_iterations()))
        self.absolute_error_text.setText(str(self.method.get_absolute_error()))
        self.execution_time_text.setText(str(self.method.get_execution_time()))


    def edit_function(self):
        self.dialog.show()

    def show_step(self, step):
        adjust_index = 1
        if self.upper_value_text.isEnabled():
            adjust_index = 0
            upper_value = round(step[1], self.round_margin)
            self.step_upper_value_text.setText(str(upper_value))

        lower_value = round(step[0], self.round_margin)
        root_value = round(step[2 - adjust_index], self.round_margin)
        absolute_error = round(step[3 - adjust_index], self.round_margin)
        self.step_lower_value_text.setText(str(lower_value))
        self.step_root_value_text.setText(str(root_value))
        self.step_absolute_error.setText(str(absolute_error))

    def next_step(self):
        if self.method is None:
            self.notification.setText("Error: Method requirements is not met.")
            return
        if self.iteration_counter < self.method.get_iterations() - 1:
            current_step = self.method.next_step()
            self.show_step(current_step)
            self.iteration_counter += 1
            self.iteration_couner_text.setText(str(self.iteration_counter))

    def previous_step(self):
        if self.method is None:
            self.notification.setText("Error: Method requirements is not met.")
            return
        if self.iteration_counter > 0:
            current_step = self.method.prev_step()
            self.show_step(current_step)
            self.iteration_counter -= 1
            self.iteration_couner_text.setText(str(self.iteration_counter))

    def adjust_criteria(self):
        try:
            self.current_absolute = float(self.absolute_error_criteria.text())
            self.current_iterations = int(self.max_iterations.text())
            self.notification.setText("Criteria is adjusted")
        except ValueError:
            self.notification.setText("ERROR: Criteria value error")

    def set_equation(self, equation):
        self.equation = equation


app = QApplication([])
window = MatPlotLibWidget()
window.show()
app.exec_()
