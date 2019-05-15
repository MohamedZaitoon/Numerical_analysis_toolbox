import time

from numpy import *

from root_finder_methods.abstract_method import Method


class Bisection(Method):

    def __init__(self, equation, lower_value, upper_value):
        self.equation = equation
        self.steps = []
        self.scale = 1
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

    def are_guesses_valid(self):
        if (self.f(self.lower_value) * self.f(self.upper_value)) > 0:
            return False
        return True

    def add_step(self):
        step = (self.lower_value, self.upper_value, self.root_value, self.absolute_error, self.f(self.lower_value),
                self.f(self.upper_value))
        self.steps.append(step)

    def evaluate(self):
        if not self.are_guesses_valid():
            self.error = True
            return
        i = 1
        self.start = time.time()
        for i in range(1, self.max_iterations_criteria):
            previous_root_value = self.root_value
            self.root_value = (self.lower_value + self.upper_value) / 2
            if i > 1:
                self.absolute_error = abs(self.root_value - previous_root_value)
            else:
                self.absolute_error = abs(self.root_value - self.lower_value)
            self.add_step()
            test = self.f(self.lower_value) * self.f(self.root_value)
            if test < 0:
                self.upper_value = self.root_value
            else:
                self.lower_value = self.root_value
            if test == 0:
                self.root_value = self.lower_value if self.f(self.lower_value) == 0 else self.root_value
                self.absolute_error = 0
                break
            if i > 1 and self.absolute_error <= self.absolute_error_criteria:
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
        step = self.steps[self.step_position]
        lower_value = step[0]
        upper_value = step[1]
        initial_step = self.steps[0]
        initial_lower = initial_step[0]
        initial_upper = initial_step[1]
        self.graph.axes.set_xlim(initial_lower - 2, initial_upper + 2)
        # self.graph.axes.set_ylim(initial_step[-2], initial_step[-1])
        self.graph.axes.axvline(lower_value, linestyle="dashed", color="r")
        self.graph.axes.axvline(upper_value, linestyle="dashed", color="g")

    def next_step(self, ):
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

    def plot(self, graph):
        self.graph = graph
        initial_step = self.steps[0]
        initial_lower = initial_step[0]
        initial_upper = initial_step[1]
        x = linspace(initial_lower - 10, initial_upper + 10, 1000)
        graph.axes.clear()
        # self.graph.axes.set_xlim(lower_value-abs(lower_value*.3), upper_value+abs(upper_value*.3))
        graph.axes.plot(x, eval(self.equation), linewidth=1)
        graph.axes.axhline(0, color="black", linewidth=1)
        graph.axes.axvline(0, color="black", linewidth=1)
        self.plot_step()
        graph.draw()

    def set_scale(self, scale):
        self.scale = scale

    def output_file(self):
        pass

    def get_errors(self):
        if len(self.steps) == 0:
            return []
        else:
            return [row[3] for row in self.steps]

    def get_roots(self):
        if len(self.steps) == 0:
            return []
        else:
            return [row[2] for row in self.steps]
