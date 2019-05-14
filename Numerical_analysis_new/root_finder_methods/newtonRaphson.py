import re
import time
import numpy as np
from scitools.StringFunction import StringFunction
from sympy import Derivative, Symbol
from root_finder_methods.abstract_method import *
from root_finder_methods.tools import loader


class NewtonRaphson(Method):

    def __init__(self, equation):
        self.x = 1
        self.replacements = {
            'sin': 'np.sin',
            'cos': 'np.cos',
            '^': '**', 'e': 'np.e', 'tan': 'np.tan', 'exp': 'np.exp'}
        self.allowed_words = ['x', 'sin', 'cos', 'tan', 'e', 'exp', 'log', 'log2']
        self.tabel = []
        self.equation = equation
        self.graph = None
        self.root = None
        self.guess = 2
        self.allowed_error: float = 0.00001
        self.maxIt = 50
        self.scale = None
        self.iterations = 0
        self.start = None
        self.end = None
        self.current = 0  # current index for next & prev

    def evaluate(self, x_guess=2):
        # handling equation
        def find(st, ch):
            return [t for t, ltr in enumerate(st) if ltr == ch]

        s = find(self.equation, 'e')
        if len(s) != 0:
            for r in s:
                if r + 1 == len(self.equation):
                    print("please replace 'e' with 'exp()' and try again!")
                    return
                else:
                    if self.equation[r + 1] != 'x':
                        print("please replace 'e' with 'exp()' and try again!")
                        return

        equation = self.equation.replace('^', '**')
        self.equation = equation
        self.guess = x_guess

        # initialize variables
        x_old: float = self.guess
        error: float = self.allowed_error + 1
        i = 0
        self.start = time.time()
        # newton_Raphson algorithm
        while float(error) > float(self.allowed_error) and i <= self.maxIt:

            f1 = float(self.__f(x_old))
            f2 = float(self.__df(x_old))
            if f2 == 0:
                self.root = None
                print("Error division by zero!")
                print("diverge")
                return
            x_new = float(x_old) - f1 / f2
            error = abs(x_new - x_old)

            self.tabel.append([i, x_old, x_new, f1, f2, error])
            print(self.tabel[i])
            self.iterations = i
            if self.__f(x_new) == 0:
                self.root = x_new
                print("--success--")
                return

            x_old = x_new
            i = i + 1
        self.end = time.time()
        if i == 51:
            self.root = None
            print("--diverge-- or need more iteration than 50")
        else:
            self.root = x_old
            print("--success--")

        return

    def set_absolute_error_criteria(self, absolute_error_criteria):
        self.allowed_error = absolute_error_criteria
        pass

    def set_max_iterations_criteria(self, max_iterations_criteria):
        self.maxIt = max_iterations_criteria
        pass

    # waiting alkhaligy
    def get_absolute_error(self):
        pass

    def get_iterations(self):
        return self.iterations

    def get_execution_time(self):
        return abs(self.end - self.start)

    # waiting alkhaligy
    def get_error(self):
        pass

    def get_root_value(self):
        return self.root

    def plot(self, graph):
        self.graph = graph
        func = self.__string2function(self.equation)
        lastx = self.tabel[len(self.tabel) - 1][2]
        if self.guess >= lastx:
            x = np.arange(lastx - 1, self.guess + 1, 0.00005)
            graph.plot([self.guess + 1, lastx - 1], [0, 0], 'k-')  # x-axis
            # graph.plot([0, 0], [self.guess + 3, lastx - 3], 'k-')  # y-axis
        else:
            x = np.arange(self.guess - 1, lastx + 1, 0.00005)
            graph.plot([self.guess - 1, lastx + 1], [0, 0], 'k-')  # x-axis
            # graph.plot([0, 0], [self.guess - 3, lastx + 3], 'k-')  # y-axis
        graph.plot(x, func(x))

        for row in self.tabel:
            graph.plot([row[1], row[2]], [func(row[1]), 0])
            graph.plot([row[1], row[1]], [0, func(row[1])])
            graph.plot([row[2], row[2]], [0, func(row[2])])
        pass

    def next_step(self):
        if self.current != len(self.tabel):
            self.current = self.current + 1
        self.__plot(self.graph, self.current)
        pass

    def prev_step(self):
        if self.current != 1:
            self.current = self.current - 1
        self.__plot(self.graph, self.current)
        pass

    def set_scale(self, scale):
        self.scale = scale

    def output_file(self):
       pass

    # additional private methods
    def __f(self, x):
        y = StringFunction(self.equation)
        return y(x)

    def __df(self, x):
        xs = Symbol('x')
        deriv = Derivative(self.equation, xs)
        dydx = deriv.doit()
        dy = StringFunction(str(dydx))
        return dy(x)

    def __plot(self, graph, idx):
        func = self.string2function(self.equation)
        lastx = self.tabel[len(self.tabel) - 1][2]
        if self.guess >= lastx:
            x = np.arange(lastx - 1, self.guess + 1, 0.00005)
            graph.plot([self.guess + 1, lastx - 1], [0, 0], 'k-')  # x-axis
            # graph.plot([0, 0], [self.guess + 3, lastx - 3], 'k-')  # y-axis
        else:
            x = np.arange(self.guess - 1, lastx + 1, 0.00005)
            graph.plot([self.guess - 1, lastx + 1], [0, 0], 'k-')  # x-axis
            # graph.plot([0, 0], [self.guess - 3, lastx + 3], 'k-')  # y-axis
        graph.plot(x, func(x))
        for i in range(0, idx):
            row = self.tabel[i]
            graph.plot([row[1], row[2]], [func(row[1]), 0])
            graph.plot([row[1], row[1]], [0, func(row[1])])
            graph.plot([row[2], row[2]], [0, func(row[2])])

    def __string2function(self, string):
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in self.allowed_words:
                raise ValueError('"{}" is forbidden to use in math expression'.format(word))
        for old, new in self.replacements.items():
            string = string.replace(old, new)

        def func(x):
            return eval(string)
        return func


if __name__ == "__main__":
    # test
    load = loader('newtonOutput.csv')
    tablet = load.getTable()
    for r in tablet:
        print(r)
