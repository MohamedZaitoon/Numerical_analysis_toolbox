import time

from numpy import *
from sympy import Poly, sympify

from root_finder_methods.abstract_method import Method


class BiergeVieta(Method):

    def __init__(self, equation, lower_value):
        self.equation = equation
        self.lower_value = lower_value
        self.steps = []
        self.root_value = None
        self.absolute_error = None
        self.error = False
        self.scale = 1
        self.start = 0
        self.end = 0
        self.graph = None
        self.iterations = 0
        self.step_position = 0
        self.max_iterations_criteria = 50
        self.absolute_error_criteria = 0.00001

    def get_coefficients(self):
        a = Poly(self.equation)
        return a.all_coeffs()

    def get_x(self):
        return self.root_value

    def add_step(self):
        step = (self.lower_value, self.root_value, self.absolute_error)
        self.steps.append(step)

    def evaluate(self):
        self.equation = sympify(self.equation)
        ai = self.get_coefficients()
        greatest_power = len(ai) - 1
        bi = [ai[0]]
        ci = [ai[0]]
        self.root_value = self.lower_value
        self.start = time.time()
        j = 0
        while j < self.max_iterations_criteria:
            for i in range(1, greatest_power + 1, 1):
                b = ai[i] + bi[i - 1] * self.root_value
                bi.append(b)
            for i in range(1, greatest_power, 1):
                c = bi[i] + ci[i - 1] * self.root_value
                ci.append(c)
            new_x = self.root_value - float(bi[len(bi) - 1]) / ci[len(ci) - 1]
            self.absolute_error = abs(new_x - self.root_value)
            self.add_step()
            if abs(new_x - self.root_value) <= self.absolute_error_criteria:
                self.lower_value = self.root_value
                self.root_value = new_x
                break
            self.lower_value = self.root_value
            self.root_value = new_x
            bi = [ai[0]]
            ci = [ai[0]]
            j = j + 1
        self.iterations = j
        self.end = time.time()

    def set_absolute_error_criteria(self, absolute_error_criteria):
        self.absolute_error_criteria = absolute_error_criteria

    def set_max_iterations_criteria(self, max_iterations_criteria):
        self.max_iterations_criteria = max_iterations_criteria

    def get_absolute_error(self):
        return self.absolute_error

    def get_iterations(self):
        return self.iterations

    def get_execution_time(self):
        return self.end - self.start

    def get_error(self):
        return self.error

    def get_root_value(self):
        return self.root_value

    def plot(self, graph):
        self.graph = graph
        step = self.steps[0]
        lower = step[0]
        upper = lower * 5 + 5
        root = self.get_root_value()
        x = linspace(int(root - 5), int(root + 5), 1000)
        graph.axes.clear()
        graph.axes.plot(x, eval(str(self.equation)), linewidth=1, color='c')
        # graph.axes.plot(x, eval(str(self.equation)), linewidth=1, color='c')
        graph.axes.axhline(0, color="black", linewidth=1)
        graph.axes.axvline(0, color="black", linewidth=1)
        self.plot_step()
        graph.draw()

    def next_step(self):
        if self.step_position == self.iterations:
            return
        self.step_position += 1
        self.plot(self.graph)
        return self.steps[self.step_position]

    def prev_step(self):
        if self.step_position == 0:
            return
        self.step_position -= 1
        self.plot(self.graph)
        return self.steps[self.step_position]

    def set_scale(self, scale):
        self.scale = scale

    def output_file(self):
        pass

    def get_errors(self):
        if len(self.steps) == 0:
            return []
        else:
            return [row[2] for row in self.steps]

    def get_roots(self):
        if len(self.steps) == 0:
            return []
        else:
            return [row[1] for row in self.steps]

    def plot_step(self):
        x = self.steps[self.step_position][1]
        self.graph.axes.axvline(x, linestyle="dashed", color="r", linewidth=1)
