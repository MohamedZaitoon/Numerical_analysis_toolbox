import re
import time
from sympy import *
from path_finder_methods.abstract_method import Method


class BiergeVieta(Method):
    def __init__(self, equation, x0):
        self.equation = equation
        self.expression = sympify(self.func)
        self.x0 = x0
        self.max_iterations_criteria = 50
        self.absolute_error_criteria = 0.00001
        self.default()
        self.ai = self.getCoeffs()
        self.greatestPower = len(self.ai) - 1
        self.bi = [self.ai[0]]
        self.ci = [self.ai[0]]
        self.currentX = x0
        self.x = [x0]
        self.errors = [""]
        self.start = time.time()
        self.solve()
        self.end = time.time()
        self.result = ""
        self.getResults()

    def evaluate(self):
        j = 0
        while j < self.self.max_iterations_criteria:
            for i in range(1, self.greatestPower + 1, 1):
                b = self.ai[i] + self.bi[i - 1] * self.currentX
                self.bi.append(b)
            for i in range(1, self.greatestPower, 1):
                c = self.bi[i] + self.ci[i - 1] * self.currentX
                self.ci.append(c)
            newX = self.currentX - float(self.bi[len(self.bi) - 1]) / self.ci[len(self.ci) - 1]
            self.x.append(newX)
            self.errors.append(100 * abs(newX - self.currentX) / float(newX))
            if abs(newX - self.currentX) <= self.self.absolute_error_criteria:
                break
            self.currentX = newX
            self.bi = [self.ai[0]]
            self.ci = [self.ai[0]]
            j = j + 1

    def set_absolute_error_criteria(self, absolute_error_criteria):
        pass

    def set_max_iterations_criteria(self, max_iterations_criteria):
        pass

    def get_absolute_error(self):
        pass

    def get_iterations(self):
        return len(self.x) - 1

    def get_execution_time(self):
        return self.end - self.start

    def get_error(self):
        pass

    def get_root_value(self):
        pass

    def plot(self, graph):
        pass

    def next_step(self):
        pass

    def prev_step(self):
        pass

    def set_scale(self, scale):
        pass

    def output_file(self):
        pass
