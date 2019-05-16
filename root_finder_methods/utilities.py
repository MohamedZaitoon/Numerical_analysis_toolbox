from .newtonRaphson import NewtonRaphson
from root_finder_methods.bierge_vieta import BiergeVieta
from root_finder_methods.bisection import Bisection
from root_finder_methods.fixed_point import FixedPoint
from root_finder_methods.secant import Secant


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
        print(content[3])
        isFloat = False
        isInt = False
        try:
            numint = int(content[3])
            isInt = True
        except Exception:
            print("float number")
        if isInt == False:
            isFloat = True
            try:
                numfl = float(content[3])
            except Exception:
                print("Invalid Number")

        # switch methods
        name = content[1]
        content[0] = content[0].replace("^", "**")
        if name.lower() == 'bisection':
            s = content[2].split()
            b = Bisection(content[0].strip(), float(s[0]), float(s[1]))
            if isFloat:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint

            return b
        elif name.lower() == 'newtonraphson':
            b = NewtonRaphson(content[0].strip(), float(content[2].strip()))
            if isFloat:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            return b
        elif name.lower() == 'fixedpoint':
            b = FixedPoint(content[0].strip(), float(content[2].strip()))
            if isFloat:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            return b
        elif name.lower() == 'secant':
            s = content[2].split()
            b = Secant(content[0].strip(), float(s[0]), float(s[1]))
            if isFloat:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            return b
        elif name.lower() == 'biergevieta':
            b = BiergeVieta(content[0].strip(), float(content[2].strip()))
            if isFloat:
                b.absolute_error_criteria = numfl
            else:
                b.max_iterations_criteria = numint
            return b
        else:
            print("Error in read file")
            return None

    def load(self):
        return self.__extract()


