import time

from numpy import *
from scitools.StringFunction import StringFunction
from sympy import Derivative, Symbol
from tabulate import tabulate

from root_finder_methods.abstract_method import Method


class NewtonRaphson(Method):

    def __init__(self, equation, x_guess=2):
        self.x = 1
        self.tabel = []
        self.equation = equation
        self.graph = None
        self.root = None
        self.guess = x_guess
        self.allowed_error: float = 0.00001
        self.maxIt = 50
        self.scale = None
        self.iterations = 0
        self.start = None
        self.end = None
        self.error = False
        self.current = 0  # current index for next & prev

    def evaluate(self):
        equation = self.equation.replace('^', '**')
        self.equation = equation

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
                self.error = True
                return
            x_new = float(x_old) - f1 / f2
            error = abs(x_new - x_old)
            self.tabel.append([x_old, x_new, error, f1, f2])
            # print(self.tabel[i])
            self.iterations = i
            if self.__f(x_new) == 0:
                self.root = x_new
                print("--success--")
                self.error = False
                return
            x_old = x_new
            i = i + 1
        self.end = time.time()
        if i == 51:
            self.root = None
            print("--diverge-- or need more iteration than 50")
            self.error = True
        else:
            self.root = x_old
            print("--success--")
            self.error = False

        return

    def set_absolute_error_criteria(self, absolute_error_criteria):
        self.allowed_error = absolute_error_criteria
        pass

    def set_max_iterations_criteria(self, max_iterations_criteria):
        self.maxIt = max_iterations_criteria
        pass

    def get_absolute_error(self):
        return self.tabel[len(self.tabel) - 1][2]

    def get_iterations(self):
        return self.iterations

    def get_execution_time(self):
        return abs(self.end - self.start)

    def get_error(self):
        return self.error

    def get_root_value(self):
        return self.root

    def plot(self, graph):
        self.graph = graph
        self.graph.axes.clear()
        lastx = self.tabel[len(self.tabel) - 1][1]
        if self.guess >= lastx:
            x = linspace(lastx - 3, self.guess + 3, 100000)
            # self.graph.axes.plot([self.guess + 1, lastx - 1], [0, 0], 'k-')  # x-axis
            # graph.plot([0, 0], [self.guess + 3, lastx - 3], 'k-')  # y-axis
        else:
            x = linspace(self.guess - 3, lastx + 3, 100000)
            # self.graph.axes.plot([self.guess - 1, lastx + 1], [0, 0], 'k-')  # x-axis
            # self.graph.axes.plot([0, 0], [self.guess - 3, lastx + 3], 'k-')  # y-axis
        self.graph.axes.plot(x, eval(self.equation))

        for i in range(0, self.current + 1):
            row = self.tabel[i]
            self.graph.axes.plot([row[0], row[1]], [self.__f(row[0]), 0])
            self.graph.axes.plot([row[0], row[0]], [0, self.__f(row[0])])
            self.graph.axes.plot([row[1], row[1]], [0, self.__f(row[1])])
        graph.axes.axhline(0, color="black")
        graph.axes.axvline(0, color="black")
        self.graph.draw()
        pass

    def next_step(self):
        if self.current != len(self.tabel):
            self.current = self.current + 1
        self.plot(self.graph)
        return self.tabel[self.current]

    def prev_step(self):
        if self.current != 0:
            self.current = self.current - 1
        self.plot(self.graph)
        return self.tabel[self.current]

    def set_scale(self, scale):
        self.scale = scale

    def output_file(self, path1):
        write = PrintToFile(path1, self.tabel)
        write.print()

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


class PrintToFile:
    def __init__(self, path, table):
        self.path = path
        self.table = table

    def print(self):
        s = tabulate(self.table, tablefmt='orgtbl')
        f = open(self.path, 'w+')
        f.write(s)
        f.close()


if __name__ == "__main__":
    # test
    t = NewtonRaphson('exp(x^2-4)', 3)
    t.evaluate()
    t.output_file('newton.txt')
    print(t.get_absolute_error())
    print(t.get_error())
