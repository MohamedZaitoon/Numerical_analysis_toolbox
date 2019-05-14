from solver.interface import Interface


class LUDecomposition(Interface):

    def __init__(self):
        self.table = []
        self.number_of_equations = 0
        self.coefficients = []
        self.constants = []
        self.result = []
        self.scaling_factors = []
        self.decomposed = []

    def calculate(self):
        self.decompose()
        d = [0] * self.number_of_equations  # {d} = {u}{x}
        # forward substitution
        for i in range(self.number_of_equations):
            for j in range(i):
                self.constants[i] = self.constants[i] - self.decomposed[i][j] * d[j]
            d[i] = self.constants[i]
        # back substitution
        for i in reversed(range(self.number_of_equations)):
            for j in reversed(range(i, self.number_of_equations)):
                d[i] = d[i] - self.decomposed[i][j] * self.result[j]
            self.result[i] = d[i] / self.decomposed[i][i]

    def get_solution(self):
        return self.result

    def get_system_type(self):
        return False

    def set_coefficients(self, coefficients, number_of_equations):
        self.coefficients = coefficients
        self.number_of_equations = number_of_equations
        for i in range(self.number_of_equations):
            row = []
            for j in range(self.number_of_equations):
                row.append(0)
            self.decomposed.append(row)

    def set_constants(self, constants):
        self.constants = constants

    def set_result(self, result):
        self.result = result

    def output_file(self):
        pass

    def input_file(self):
        pass

    def decompose(self):
        for i in range(self.number_of_equations - 1):
            for j in range(i + 1, self.number_of_equations):
                factor = self.coefficients[j][i] / self.coefficients[i][i]
                self.decomposed[j][i] = factor
                self.coefficients[j][i] = 0
                for k in range(i + 1, self.number_of_equations):
                    self.coefficients[j][k] = self.coefficients[j][k] - factor * self.coefficients[i][k]
        for i in range(self.number_of_equations):
            for j in range(i, self.number_of_equations):
                self.decomposed[i][j] = self.coefficients[i][j]
