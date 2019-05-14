from tabulate import tabulate
from root_finder_methods.secant import Secant
from root_finder_methods.fixed_point import FixedPoint
from root_finder_methods.bisection import Bisection
from root_finder_methods.newtonRaphson import NewtonRaphson
from root_finder_methods.bierge_vieta import BiergeVieta


class Loader:
    def __init__(self, path):
        self.path = path

    def setpath(self, path):
        self.path = path

    def __extract(self):
        with open(self.path) as f:
            content = f.readlines()
        content = [x.strip() for x in content]

        # error or max iterations
        numint = int(content[3])
        numfl = float(content[3])

        # switch methods
        name = content[1]
        if name.lower() == 'bisection':
            b = Bisection
            b.equation = content[0].strip()
            if str(numfl) == content[3]:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            s = content[2].split()
            b.lower_value = float(s[0])
            b.upper_value = float(s[1])
            return b
        elif name.lower() == 'newtonraphson':
            b = NewtonRaphson
            b.equation = content[0].strip()
            if str(numfl) == content[3]:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            b.guess = float(content[2].strip())
            return b
        elif name.lower() == 'fixedpoint':
            b = FixedPoint
            b.equation = content[0].strip()
            if str(numfl) == content[3]:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            b.lower_value = float(content[2].strip())
            return b
        elif name.lower() == 'secant':
            b = Secant
            b.equation = content[0].strip()
            if str(numfl) == content[3]:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            s = content[2].split()
            b.lower_value = float(s[0])
            b.upper_value = float(s[1])
            return b
        elif name.lower() == 'biergevieta':
            b = BiergeVieta
            b.equation = content[0].strip()
            if str(numfl) == content[3]:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            b.lower_value = float(content[2].strip())
            return b
        else:
            print("Error in read file")
            return None

    def load(self):
        return self.__extract()


class PrintToFile:
    def __init__(self, path, table):
        self.path = path
        self.table = table

    def print(self):
        s = tabulate(self.table, tablefmt='orgtbl')
        f = open(self.path, 'w+')
        f.write(s)
        f.close()
