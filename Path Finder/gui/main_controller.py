from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
from numpy import *
from path_finder_methods.bisection import Bisection
from path_finder_methods.secant import Secant
from path_finder_methods.bierge_vieta import BiergeVieta
from path_finder_methods.fixed_point import FixedPoint


class MatPlotLibWidget(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("main_window.ui", self)
        self.method = None
        self.equation = None
        layout = QVBoxLayout()
        layout.addWidget(NavigationToolbar(self.MplWidget.canvas, self))
        self.graph_adjustments.setLayout(layout)
        self.solve_button.clicked.connect(self.solve)
        self.next_step_button.clicked.connect(self.next_step)
        self.previous_step_button.clicked.connect(self.previous_step)
        self.adjust_criteria_button.clicked.connect(self.adjust_criteria)
        self.selected_method.activated.connect(self.adjust_parameters)

        self.scale_slider.setTickInterval(100)
        self.scale_slider.setMinimum(0)
        self.scale_slider.setSingleStep(1)
        self.scale_slider.sliderMoved.connect(self.slider_moved)
        self.scale = 1

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

        self.method.set_absolute_error_criteria(self.current_absolute)
        self.method.set_max_iterations_criteria(self.current_iterations)
        self.method.set_scale(self.scale)
        try:
            self.method.evaluate()
            if self.method.get_error():
                self.notification.setText("Method Error: Invalid guesses or divergence may occurred")
                return

            self.method.plot(self.MplWidget.canvas)
            self.show_results()
        except Exception:
            self.notification.setText("Error")

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
        two_parameter_method = ("Bisection", "Secant")
        one_parameter_method = ("Bierge-Vieta", "Fixed Point")
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

    def slider_moved(self):
        value = self.scale_slider.value()
        self.scale = value
        self.scale_text.setText(str(value))

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


class EquationForm(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self)
        loadUi("equation_form.ui", self)
        self.main_window = main_window
        self.equation = ""
        self.equation_text.setText("")
        self.free_style = False

        self.variable_x_button.clicked.connect(self.variable_x)
        self.clear_button.clicked.connect(self.clear)
        self.square_root_button.clicked.connect(self.square_root)
        self.pi_button.clicked.connect(self.pi)
        self.left_bracket_button.clicked.connect(self.left_bracket)
        self.right_bracket_button.clicked.connect(self.right_bracket)

        self.button_0.clicked.connect(self.zero)
        self.button_1.clicked.connect(self.one)
        self.button_2.clicked.connect(self.two)
        self.button_3.clicked.connect(self.three)
        self.button_4.clicked.connect(self.four)
        self.button_5.clicked.connect(self.five)
        self.button_6.clicked.connect(self.six)
        self.button_7.clicked.connect(self.seven)
        self.button_8.clicked.connect(self.eight)
        self.button_9.clicked.connect(self.nine)

        self.dot_button.clicked.connect(self.dot)
        self.divide_button.clicked.connect(self.divide)
        self.multiply_button.clicked.connect(self.multiply)
        self.subtract_button.clicked.connect(self.subtract)
        self.add_button.clicked.connect(self.add)

        self.sin_button.clicked.connect(self.sin)
        self.cosine_button.clicked.connect(self.cos)
        self.tan_button.clicked.connect(self.tan)
        self.sinh_button.clicked.connect(self.sinh)
        self.cosh_button.clicked.connect(self.cosh)
        self.tanh_button.clicked.connect(self.tanh)
        self.arcsin_button.clicked.connect(self.arcsin)
        self.arccos_button.clicked.connect(self.arccos)
        self.arctan_button.clicked.connect(self.arctan)

        self.power_button.clicked.connect(self.power)
        self.log_button.clicked.connect(self.log)
        self.exp_button.clicked.connect(self.exp)
        self.comma_button.clicked.connect(self.comma)

        self.delete_button.clicked.connect(self.delete)
        self.submit_button.clicked.connect(self.submit)
        self.validity_button.clicked.connect(self.check_validity)
        self.free_style_button.clicked.connect(self.activate_free_style)

    def variable_x(self):
        self.equation += "x"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "x")

    def clear(self):
        self.equation = ""
        self.equation_text.setText("")
        self.notification_text.setText("")

    def square_root(self):
        self.equation += "sqrt("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "sqrt(")

    def pi(self):
        self.equation += "pi"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "π")

    def left_bracket(self):
        self.equation += "("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "(")

    def right_bracket(self):
        self.equation += ")"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + ")")

    def zero(self):
        self.equation += "0"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "0")

    def one(self):
        self.equation += "1"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "1")

    def two(self):
        self.equation += "2"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "2")

    def three(self):
        self.equation += "3"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "3")

    def four(self):
        self.equation += "4"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "4")

    def five(self):
        self.equation += "5"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "5")

    def six(self):
        self.equation += "6"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "6")

    def seven(self):
        self.equation += "7"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "7")

    def eight(self):
        self.equation += "8"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "8")

    def nine(self):
        self.equation += "9"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "9")

    def dot(self):
        self.equation += "."
        self.equation_text.setText(str(self.equation_text.toPlainText()) + ".")

    def divide(self):
        self.equation += "/"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "/")

    def multiply(self):
        self.equation += "*"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "*")

    def subtract(self):
        self.equation += "-"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "-")

    def add(self):
        self.equation += "+"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "+")

    def sin(self):
        self.equation += "sin("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "sin(")

    def cos(self):
        self.equation += "cos("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "cos(")

    def tan(self):
        self.equation += "tan("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "tan(")

    def sinh(self):
        self.equation += "sinh("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "sinh(")

    def cosh(self):
        self.equation += "cosh("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "cosh(")

    def tanh(self):
        self.equation += "tan("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "tanh(")

    def arcsin(self):
        self.equation += "arcsin("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "arcsin(")

    def arccos(self):
        self.equation += "arccos("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "arccos(")

    def arctan(self):
        self.equation += "arctan("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "arctan(")

    def power(self):
        self.equation += "**"
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "^")

    def log(self):
        self.equation += "log("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "log(")

    def exp(self):
        self.equation += "exp("
        self.equation_text.setText(str(self.equation_text.toPlainText()) + "exp(")

    def comma(self):
        self.equation += ","
        self.equation_text.setText(str(self.equation_text.toPlainText()) + ",")

    def delete(self):
        if self.equation == "":
            return
        self.equation = self.equation[:-1]
        self.equation_text.setText(str(self.equation_text.toPlainText())[:-1])

    def activate_free_style(self):
        self.free_style = not self.free_style
        self.equation_text.setEnabled(self.free_style)

    def check_validity(self):
        try:
            if self.free_style:
                self.equation = str(self.equation_text.toPlainText()).replace("^", "**")
            eval(self.equation, None, {'x': 0})
            self.notification_text.setText("Valid Equation")
            return True
        except RuntimeWarning:
            self.notification_text.setText("Warning: Zero must be avoided for either division or log..etc")
            return True
        except ZeroDivisionError:
            self.notification_text.setText("Error: Zero division")
            return
        except NameError:
            self.notification_text.setText("ERROR: Equation is invalid")
            return
        except SyntaxError:
            self.notification_text.setText("ERROR: Equation is invalid")
            return

    def submit(self):
        if not self.check_validity():
            return
        self.main_window.set_equation(self.equation)
        self.close()


app = QApplication([])
window = MatPlotLibWidget()
window.show()
app.exec_()
