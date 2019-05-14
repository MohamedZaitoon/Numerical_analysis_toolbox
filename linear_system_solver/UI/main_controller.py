from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from numpy import *
from time import time

from UI.scenes.parser import Parser
from solver.gauss_elimination import GaussElimination
from solver.LU_decomposition import LUDecomposition
from solver.gauss_jordan import GaussJordan
from solver.gauss_seidel import GaussSeidel
from UI.steps_window_controller import IterativeSteps
from UI.plot_window import PlotWindow


class MainController(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        loadUi("scenes/main_window.ui", self)

        self.is_solution_table_occupied = False
        self.is_iterative_method = False
        self.method = None
        self.start = None
        self.end = None

        self.equations = []
        self.coefficients = []
        self.constants = []
        self.result = []
        self.initial_guesses = []

        self.parser = Parser()
        self.plot_window = PlotWindow(self)

        self.solve_button.clicked.connect(self.solve)
        self.clear_all_button.clicked.connect(self.clear_all)
        self.selected_method.activated.connect(self.adjust_type)
        self.adjust_criteria_button.clicked.connect(self.adjust_criteria)
        self.insert_equation_button.clicked.connect(self.insert_equation)
        self.delete_equation_button.clicked.connect(self.delete_equation)
        self.clear_equations_button.clicked.connect(self.delete_equations)
        self.steps_button.clicked.connect(self.show_iterative_steps)
        self.delete_initial_guess_button.clicked.connect(self.delete_initial_guesses)
        self.insert_initial_guesses_button.clicked.connect(self.add_initial_guesses)
        self.plot_button.clicked.connect(self.show_plot)

        self.equations_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.insert_initial_guesses_table_widget.setSelectionBehavior(QAbstractItemView.SelectColumns)

        self.number_of_equations = 0
        self.initial_guesses_counter = 0
        self.current_absolute = 0.00001
        self.current_iterations = 50

        self.adjust_type()

    def solve(self):
        self.adjust_type()
        selected_method = self.selected_method.currentText()
        self.clear_all()

        self.parser.tabulate_equations()
        self.coefficients = self.parser.get_coefficients()
        self.result = self.parser.get_result()
        self.constants = self.parser.get_constants()

        if self.is_iterative_method:
            if self.initial_guesses_counter != self.number_of_equations:
                self.notification_text.setText("Insufficient or excessive initial guesses")
                return

        self.start = time()
        if selected_method == "Gaussian-elimination":
            self.method = GaussElimination()
        elif selected_method == "LU decomposition":
            self.method = LUDecomposition()
        elif selected_method == "Gaussian-Jordan":
            self.method = GaussJordan()
        else:
            self.method = GaussSeidel(self.current_absolute, self.current_iterations, self.initial_guesses)

        self.is_solution_table_occupied = True
        self.end = time()

        self.method.set_coefficients(self.coefficients, self.number_of_equations)
        self.method.set_constants(self.constants)
        self.method.set_result(self.result)
        try:
            self.method.calculate()
        except Exception:
            self.notification_text.setText("ERROR")

        self.insert_result()

    def show_plot(self):
        self.plot_window.show()

    def show_iterative_steps(self):
        iterative_steps = IterativeSteps(self)
        iterative_steps.

    def add_initial_guesses(self):
        try:
            guess = float(self.insert_initial_guesses_text.text())
            self.initial_guesses.append(guess)
            self.insert_initial_guesses_table_widget.insertColumn(self.initial_guesses_counter)
            self.insert_initial_guesses_table_widget.setItem(0, self.initial_guesses_counter,
                                                             QTableWidgetItem(f"x{self.initial_guesses_counter}"))
            self.insert_initial_guesses_table_widget.setItem(1, self.initial_guesses_counter,
                                                             QTableWidgetItem(str(guess)))
            self.initial_guesses_counter += 1
        except ValueError:
            self.notification_text.setText("Initial Guesses Value Error")

    def delete_initial_guesses(self):
        self.initial_guesses.clear()
        if self.initial_guesses_counter != 0:
            for i in range(self.initial_guesses_counter):
                self.insert_initial_guesses_table_widget.removeColumn(0)
        self.initial_guesses_counter = 0

    def adjust_type(self):
        non_iterative_method = ["Gaussian-elimination", "LU decomposition", "Gaussian-Jordan"]

        selected_method = self.selected_method.currentText()

        if non_iterative_method.count(selected_method) != 0:
            self.is_iterative_method = False
        else:
            self.is_iterative_method = True

        flag = self.is_iterative_method

        self.epislon_criteria_text.setEnabled(flag)
        self.steps_button.setEnabled(flag)
        self.max_iterations_criteria_text.setEnabled(flag)
        self.adjust_criteria_button.setEnabled(flag)
        self.insert_initial_guesses_text.setEnabled(flag)
        self.insert_initial_guesses_button.setEnabled(flag)
        self.delete_initial_guess_button.setEnabled(flag)

    def delete_equation(self):
        selected = self.equations_table_widget.currentRow()
        if selected < 0:
            self.notification_text.setText("Selection Error: Select Equation")
            return
        if selected == self.number_of_equations:
            return
        self.number_of_equations -= 1
        self.parser.delete_equation(selected)
        self.equations_table_widget.removeRow(selected)

    def delete_equations(self):
        for i in range(self.number_of_equations):
            self.equations_table_widget.removeRow(0)
        self.parser.clear_parser()
        self.initial_guesses.clear()
        self.number_of_equations = 0

    def clear_all(self):
        if self.is_solution_table_occupied and self.solution_table_widget.rowCount() != 1:
            for i in range(self.solution_table_widget.rowCount() - 1):
                self.solution_table_widget.removeRow(0)
        if self.insert_initial_guesses_table_widget.columnCount() != 1:
            for i in range(self.insert_initial_guesses_table_widget.columnCount() - 1):
                self.insert_initial_guesses_table_widget.removeColumn(0)
            self.initial_guesses_counter = 0
        self.execution_time_text.setText("")
        self.notification_text.setText("")

    def insert_result(self):
        result = self.method.get_solution()
        for i in range(self.number_of_equations):
            self.solution_table_widget.insertRow(i)
            self.solution_table_widget.setItem(i, 0, QTableWidgetItem(f"x{i}"))
            self.solution_table_widget.setItem(i, 1, QTableWidgetItem(str(result[i])))
        self.execution_time_text.setText(str(self.end - self.start))

    def insert_equation(self):
        equation = str(self.insert_equation_text.text()).replace(" ", "")
        if equation == "":
            self.notification_text.setText("Input Error: NULL INPUT")
            return
        try:
            self.notification_text.setText(str(self.parser.add_equation(equation)))
            if self.number_of_equations != self.parser.get_number_of_equations():
                self.number_of_equations = self.parser.get_number_of_equations()
                self.equations_table_widget.insertRow(self.number_of_equations)
                self.equations_table_widget.setItem(self.number_of_equations - 1, 0, QTableWidgetItem(
                    equation.replace(" ", "")))
        except IndexError:
            self.notification_text.setText("Index Error")

    def adjust_criteria(self):
        try:
            self.current_absolute = float(self.epislon_criteria_text.text())
            self.current_iterations = int(self.max_iterations_criteria_text.text())
            self.notification_text.setText("Criteria is adjusted")
        except ValueError:
            self.notification_text.setText("ERROR: Criteria value error")


app = QApplication([])
window = MainController()
window.show()
app.exec_()
