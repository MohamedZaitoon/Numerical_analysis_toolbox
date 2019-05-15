import time

from numpy import *
from sympy import simplify, sympify

from root_finder_methods.abstract_method import Method


class FixedPoint(Method):

    def __init__(self, equation, lower_value):
        self.equation = equation
        self.lower_value = lower_value  # initial x0
        self.graph = None
        self.steps = []
        self.root_value = None
        self.absolute_error = None
        self.error = False
        self.g = ""
        self.scale = 1
        self.start = 0
        self.end = 0
        self.step_position = 0
        self.iterations = 0
        self.max_iterations_criteria = 50
        self.absolute_error_criteria = 0.00001

    def get_g(self, equation):
        g = equation + " + x"
        g = str(simplify(g))
        self.g = g
        return g

    def f(self, x):
        return eval(str(self.equation), None, {'x': x})

    def add_step(self, new_x):
        step = (self.lower_value, new_x, self.absolute_error)
        self.steps.append(step)

    def evaluate(self):
        equation = self.equation
        self.equation = sympify(equation)
        self.start = time.time()
        g = self.get_g(equation)
        self.g = g
        x = self.lower_value  # initial x0
        self.root_value = self.lower_value
        j = 0
        while j < self.max_iterations_criteria:
            new_x = float(eval(g))
            self.absolute_error = abs(new_x - x)
            self.add_step(new_x)
            if self.absolute_error <= self.absolute_error_criteria:
                self.lower_value = self.root_value
                self.root_value = round(new_x, 15)
                break
            self.lower_value = new_x
            self.root_value = round(new_x, 15)
            x = new_x
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

    def plot_step(self):
        y = 0
        for i in range(self.step_position):
            step = self.steps[i]
            xi = step[0]
            xin = step[1]
            self.graph.axes.plot((xi, xi), (y, xin), 'y', linewidth=1)
            self.graph.axes.plot((xi, xin), (xin, xin), 'y', linewidth=1)
            y = xin
        step = self.steps[self.step_position]
        xi = step[0]
        xin = step[1]
        self.graph.axes.plot((xi, xi), (y, xin), 'g')
        self.graph.axes.plot((xi, xin), (xin, xin), 'r')
        # step = self.steps[self.step_position]
        # lower_value = step[0]
        # upper_value = lower_value * 5 * self.scale
        # initial_step = self.steps[0]
        # initial_lower = initial_step[0]
        # initial_upper = initial_lower * 5 * self.scale
        # graph_x_min = (self.f(initial_lower - fabs(initial_upper) * self.scale)
        #                + lower_value - fabs(upper_value) * self.scale) / 2
        # graph_x_max = (self.f(initial_upper + fabs(initial_upper) * self.scale)
        #                + upper_value + fabs(upper_value) * self.scale) / 2
        # x = linspace(graph_x_min, graph_x_max, 1000)
        #
        # self.graph.axes.plot(x, eval(str(self.g)), linestyle="dashed")
        # self.graph.draw()

    def plot(self, graph):
        self.graph = graph
        step = self.steps[0]
        lower = step[0]
        upper = lower * 5 + 5
        root = self.get_root_value()
        x = linspace(root - 5,
                     root + 5, 1000)
        graph.axes.clear()
        graph.axes.plot(x, eval(str(self.g)), linewidth=1, color='c')
        # graph.axes.plot(x, eval(str(self.equation)), linewidth=1, color='c')
        graph.axes.plot(x, x, color='m', linewidth=1)
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
