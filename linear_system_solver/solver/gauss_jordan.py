from solver.interface import Interface


class GaussJordan(Interface):

    def __init__(self):
        self.table = []
        self.coefficients = []
        self.constants = []
        self.result = []
        self.number_of_equations = 0

    def calculate(self):
        for i in range(self.number_of_equations):
            self.scale(i)
            for j in range(self.number_of_equations):
                if j != i:
                    factor = self.coefficients[j][i]
                    self.coefficients[j][i] = 0
                    for k in range(i + 1, self.number_of_equations):
                        self.coefficients[j][k] = self.coefficients[j][k] - factor * self.coefficients[i][k]
                    self.constants[j] = self.constants[j] - factor * self.constants[i]
        i = self.number_of_equations - 1
        self.result = self.constants

    def get_solution(self):
        return self.result

    def get_system_type(self):
        return False

    def set_coefficients(self, coefficients, number_of_equations):
        self.coefficients = coefficients
        self.number_of_equations = number_of_equations

    def set_constants(self, constants):
        self.constants = constants

    def set_result(self, result):
        self.result = result

    def output_file(self):
        pass

    def input_file(self):
        pass

    def scale(self, i):
        for j in range(i + 1, self.number_of_equations):
            self.coefficients[i][j] = self.coefficients[i][j] / self.coefficients[i][i]
        self.constants[i] = self.constants[i] / self.coefficients[i][i]
        self.coefficients[i][i] = 1

