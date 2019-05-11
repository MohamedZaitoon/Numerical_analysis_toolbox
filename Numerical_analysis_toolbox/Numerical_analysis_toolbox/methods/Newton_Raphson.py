import re
import csv
import os
import numpy as np
from math import *
from scitools.StringFunction import StringFunction
from sympy import Derivative, Symbol
from methods.abstractMethod import *


class NewtonRaphson(Method):

    def __init__(self):
        self.x = 1
        self.replacements = {
            'sin': 'np.sin',
            'cos': 'np.cos',
            '^': '**', 'e': 'np.e', 'tan': 'np.tan', 'exp': 'np.exp'}
        self.allowed_words = ['x', 'sin', 'cos', 'tan', 'e', 'exp', 'log', 'log2']
        self.safe_dict = {'sin': sin, 'cos': cos, 'tan': tan, 'e': e, 'sqrt': sqrt, 'log': log10, 'log2': log2,
                          'pi': pi, 'sinh': sinh, 'cosh': cosh, 'tanh': tanh, 'acos': acos, 'asin': asin,
                          'atan': atan, 'rad': radians, 'deg': degrees, 'x': 1, 'exp': exp}
        self.tabel = []
        self.equation = None
        self.root = None
        self.guess = 1
        self.current = 0  # current index for undo & redo

    def f(self, x):
        y = StringFunction(self.equation)
        return y(x)

    def df(self, x):
        xs = Symbol('x')
        deriv = Derivative(self.equation, xs)
        dydx = deriv.doit()
        dy = StringFunction(str(dydx))
        return dy(x)

    def set_equation(self, equation: str):
        self.equation = equation

    def calculate(self, equation: str, x_guess=1, it=50, eps=0.000000001):
        # handling equation
        def find(st, ch):
            return [t for t, ltr in enumerate(st) if ltr == ch]

        s = find(equation, 'e')
        if len(s) != 0:
            for r in s:
                if r + 1 == len(equation):
                    print("please replace 'e' with 'exp()' and try again!")
                    return
                else:
                    if equation[r + 1] != 'x':
                        print("please replace 'e' with 'exp()' and try again!")
                        return

        equation = equation.replace('^', '**')
        self.set_equation(equation)
        self.guess = x_guess

        # initialize variables
        x_old: float = x_guess
        error: float = eps + 1
        i = 0

        # newton_Raphson algorithm
        while float(error) > float(eps) and i <= it:

            if self.df(x_old) == 0:
                self.root = None
                print("Error division by zero!")
                print("diverge")
                return None

            x_new = float(x_old) - float(self.f(x_old)) / float(self.df(x_old))
            error = abs(x_new - x_old)

            self.tabel.append([i, x_old, x_new, self.f(x_old), self.df(x_old), error])
            print(self.tabel[i])
            if self.f(x_new) == 0:
                self.root = x_new
                print("--success--")
                return self.root

            x_old = x_new
            i = i + 1

        if i == 51:
            self.root = None
            print("--diverge-- or need more iteration than 50")
        else:
            self.root = x_old
            print("--success--")

        return self.root

    def plot(self, graph):
        if self.equation is None:
            return
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
        # li = []
        # for i in x:
        #   li.append(self.f(i))
        # y = np.array(li)
        # ymax = np.amax(y)
        graph.plot(x, func(x))

        for row in self.tabel:
            graph.plot([row[1], row[2]], [func(row[1]), 0])
            graph.plot([row[1], row[1]], [0, func(row[1])])
            graph.plot([row[2], row[2]], [0, func(row[2])])

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

    def next_step(self, graph):
        if self.current != len(self.tabel):
            self.current = self.current + 1
        self.__plot(graph, self.current)

    def prev_step(self, graph):
        if self.current != 1:
            self.current = self.current - 1
        self.__plot(graph, self.current)

    def get_root_values(self):
        return self.root

    def get_iteration(self, index):
        return self.tabel[index]

    def get_error(self):
        # return error that calculated during calculating root
        super().get_error()

    def output_file(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, 'newtonOutput.csv')
        with open(filename, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter='|')
            writer.writerow(["Iteration", "X(i)", "X(i+1)", "f(Xi)", "f’(Xi)", "AbsError"])
            for row in self.tabel:
                writer.writerow(row)

    def string2function(self, string):
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in self.allowed_words:
                raise ValueError('"{}" is forbidden to use in math expression'.format(word))
        for old, new in self.replacements.items():
            string = string.replace(old, new)

        def func(x):
            return eval(string)
        return func


if __name__ == "__main__":
    test = NewtonRaphson()
    # print(test.calculate('4*x^2 + e^x + 3*x'))
    # print(test.tabel)
    # print(test.calculate('4*x^2 + 3*x - 4', 10))
    # print(test.calculate('cos(x)', 1))
    # test.output_file()
