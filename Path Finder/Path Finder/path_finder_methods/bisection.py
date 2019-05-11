import numpy as np
from path_finder_methods.abstract_method import Method
import time


class Bisection(Method):
    steps = []

    def __init__(self, equation, lower_value,  upper_value):
        self.equation = equation
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
        step = (self.lower_value, self.upper_value, self.root_value, self.absolute_error)
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
                self.absolute_error = np.abs(self.root_value - previous_root_value)
            else:
                self.absolute_error = np.abs(self.root_value - self.lower_value)
            self.add_step()
            test = self.f(self.lower_value) * self.f(self.root_value)
            if test < 0:
                self.upper_value = self.root_value
            else:
                self.lower_value = self.root_value
            if test == 0:
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
        x = np.linspace((self.f(initial_lower - np.fabs(initial_upper) * self.scale)
                        + lower_value - np.fabs(upper_value) * self.scale) / 2,
                        (self.f(initial_upper + np.fabs(initial_upper) * self.scale)
                         + upper_value + np.fabs(upper_value) * self.scale) / 2, 10)
        self.graph.axes.plot(lower_value + x * 0, x, linestyle="dashed")
        self.graph.axes.plot(upper_value + x * 0, x, linestyle="dashed")
        self.graph.axes.plot(x, x * 0, linestyle='dotted')
        self.graph.draw()

    def next_step(self,):
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
        step = self.steps[self.step_position]
        lower = step[0]
        upper = step[1]
        x = np.linspace(lower - np.fabs(upper) * self.scale,
                        upper + np.fabs(upper) * self.scale, 1000)
        graph.axes.clear()
        graph.axes.plot(x, eval(self.equation))
        self.plot_step()
        graph.draw()

    def set_scale(self, scale):
        self.scale = scale

    def output_file(self):
        pass
