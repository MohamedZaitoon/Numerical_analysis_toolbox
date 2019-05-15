from numpy import *
from root_finder_methods.abstract_method import Method
import time


class Secant(Method):

    def __init__(self, equation, lower_value,  upper_value):
        self.equation = equation
        self.scale = 1
        self.steps = []
        self.graph = None
        self.step_position = 0
        self.lower_value = lower_value
        self.upper_value = upper_value
        self.root_value = None
        self.iterations = 0
        self.absolute_error = None
        self.error = False
        self.absolute_error_criteria = 0.00001
        self.max_iterations_criteria = 50
        self.start = 0
        self.end = 0

    def f(self, x):
        return eval(self.equation, None, {'x': x})

    def add_step(self):
        step = (self.lower_value, self.upper_value, self.root_value, self.f(self.root_value), self.absolute_error, self.f(self.lower_value),
                self.f(self.upper_value))
        self.steps.append(step)

    def evaluate(self):
        self.start = time.time()
        i = 1
        for i in range(1, self.max_iterations_criteria):
            previous_root_value = self.root_value
            self.root_value = self.upper_value - (self.f(self.upper_value) *
                                                  (self.lower_value - self.upper_value))/(self.f(self.lower_value)
                                                                                          - self.f(self.upper_value))
            if i > 1:
                self.absolute_error = abs(self.root_value - previous_root_value)
            else:
                self.absolute_error = abs(self.root_value - self.upper_value)
            self.add_step()
            self.lower_value = self.upper_value
            self.upper_value = self.root_value
            if i > 1 and self.absolute_error <= self.absolute_error_criteria or self.absolute_error == 0:
                break
        self.end = time.time()
        self.iterations = i

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
        for i in range(self.step_position):
            step = self.steps[i]
            lower_value = step[0]
            upper_value = step[1]
            flower = step[-2]
            fupper = step[-1]
            current_root = step[2]
            # x = linspace(lower_value, upper_value, 1000)
            # coefficient = (fupper - flower) / (upper_value - lower_value)
            self.graph.axes.plot((lower_value, upper_value), (flower, fupper), linestyle="dashed", color="y", linewidth=1)
            self.graph.axes.plot((current_root, current_root), (0, self.f(current_root)), color='r', linewidth=1)

            # self.graph.axes.plot((lower_value, upper_value), (flower, fupper), 'r')
            # self.graph.axes.plot((current_root, current_root), (0, self.f(current_root)), 'r')
        step = self.steps[self.step_position]
        lower_value = step[0]
        upper_value = step[1]
        flower = step[-2]
        fupper = step[-1]
        self.graph.axes.plot((lower_value, upper_value), (flower, fupper), linestyle="dashed", color="g")
        # step = self.steps[self.step_position]
        # lower_value = step[0]
        # upper_value = step[1]
        # initial_step = self.steps[0]
        # initial_lower = initial_step[0]
        # initial_upper = initial_step[1]
        # x = linspace(initial_lower, initial_upper, 10)
        # # self.graph.axes.set_xlim(graph_x_min, graph_x_max)
        # # self.graph.axes.set_ylim(graph_x_min, graph_x_max)
        # coefficient = (steps[-2]- self.f(lower_value)) / (upper_value - lower_value)
        # self.graph.axes.plot(x, (x - lower_value) * coefficient + self.f(lower_value), linestyle="dashed")
        # self.graph.axes.plot(x, x * 0, linestyle='dotted')
        # self.graph.draw()

    def plot(self, graph):
        self.graph = graph
        step = self.steps[0]
        lower = step[0]
        upper = step[1]
        x = linspace(lower, upper, 10000)
        graph.axes.clear()
        graph.axes.plot(x, eval(self.equation), linewidth=1)
        self.plot_step()
        graph.axes.axhline(0, color="k", linewidth=1)
        graph.axes.axvline(0, color="k", linewidth=1)
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
            return [row[4] for row in self.steps]

    def get_roots(self):
        if len(self.steps) == 0:
            return []
        else:
            return [row[2] for row in self.steps]

