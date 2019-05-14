import re


class Parser:
    def __init__(self):
        self.is_tabulated = False
        self.number_of_equations = 0
        self.equations = []
        self.coefficients = []
        self.constants = []
        self.result = []

    def get_number_of_equations(self):
        return self.number_of_equations

    def get_coefficients(self):
        return self.coefficients

    def get_constants(self):
        return self.constants

    def get_result(self):
        return self.result

    def get_equations(self):
        return self.equations

    def add_equation(self, equation):
        equation = str(equation.replace(" ", ""))
        if re.search(r'[a-w]|[yz]', equation) or re.search(r'(^x[\d]{0}$)', equation):
            return "Equation Error: variables should be in xi form"
        if re.search(r'(?!(?:\+-|-\+|=-|=\+))[+*/\-=]{2,}', equation):
            return "Equation Error: Operators can't be consecutive"
        if not re.search(r'=', equation):
            return "Equation Error: INVALID EQUATION"
        self.number_of_equations += 1
        self.equations.append(equation)
        return "Equation is added"

    def delete_equation(self, index):
        self.number_of_equations -= 1
        self.equations.pop(index)
        if self.is_tabulated:
            self.coefficients.pop(index)
            self.constants.pop(index)
            self.result.pop(index)

    def clear_parser(self):
        self.number_of_equations = 0
        self.equations.clear()
        self.constants.clear()
        self.coefficients.clear()
        self.result.clear()

    def tabulate_equations(self):
        self.result = []
        self.constants = []
        self.coefficients = []
        j = 0
        var = None
        while j < self.number_of_equations:
            i = 0
            row = []
            while i < self.number_of_equations:
                var = "x" + str(i)
                eq = self.equations[j]
                s = re.search(r'-?\d+\.\d+{}|-?\d+{}|-?{}'.format(var, var, var), eq)
                if s:
                    coefficient = s.group()
                    coefficient = coefficient.replace(var, "")
                    if coefficient == '-' or coefficient == '':
                        coefficient = coefficient + '1'
                    row.append(float(coefficient))
                else:
                    if var in eq:
                        row.append(1.0)
                    else:
                        row.append(0)
                i = i + 1
            self.coefficients.append(row)
            j = j + 1
        i = 0
        while i < self.number_of_equations:
            eq = self.equations[i]
            s = re.search(r'=-?\d+\.\d+|\b=-?\d+'.format(var), eq)
            constant = s.group()
            constant = constant.replace('=', '')
            self.constants.append(float(constant))
            i = i + 1
        for i in range(self.number_of_equations):
            self.result.append(0)
        self.is_tabulated = True
