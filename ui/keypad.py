from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi
from numpy import *


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
