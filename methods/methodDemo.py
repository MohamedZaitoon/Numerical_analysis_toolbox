from methods.abstractMethod import *
import numpy as np


class Demo(Method):

    def calculate(self, equation, it=50, eps=0.00001):
        # implementation of a methode
        pass

    def plot(self, graph):
        r = np.random.rand(10)
        print(r)
        graph.plot(r, np.tan(r), ".")

    def next_step(self, graph):
        # plot the next step
        pass

    def prev_step(self, graph):
        # plot the previous step
        pass

    def get_root_values(self):
        # return root values that calculated during calculating root
        pass

    def get_iteration(self):
        # return iterations
        pass

    def get_error(self):
        # return error that calculated during calculating root
        super().get_error()

    def output_file(self):
        # write the output of this method in a file "tabular format" -it may be a general method-
        pass
