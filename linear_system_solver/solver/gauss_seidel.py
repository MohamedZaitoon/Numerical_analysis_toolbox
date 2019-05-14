from solver.interface import Interface


class GaussSeidel(Interface):

    def __init__(self, es, max_itr, initial_guesses):
        self.table = []
        self.number_of_equations = 0
        self.es = es
        self.max_itr = max_itr
        self.coefficients = []
        self.constants = []
        self.result = []
        self.initial_guesses = initial_guesses

    def calculate(self):
        itr = 0
        while True and itr < self.max_itr:
            previous = []
            for i in range(self.number_of_equations):
                previous.append(self.result[i])
            self.table.append(previous)
            for i in range(self.number_of_equations):
                cons = self.constants[i]
                for j in range(self.number_of_equations):
                    if i != j:
                        cons = cons - self.coefficients[i][j] * self.result[j]
                self.result[i] = cons / self.coefficients[i][i]
            if self.exceed(previous):
                break
            itr = itr + 1
        self.table.append(self.result)

    def get_solution(self):
        return self.result

    def get_system_type(self):
        return False

    def set_coefficients(self, coefficients, number_of_equations):
        self.coefficients = coefficients
        self.number_of_equations = number_of_equations
        for i in range(self.number_of_equations):
            self.result.append(self.initial_guesses[i])

    def set_constants(self, constants):
        self.constants = constants

    def set_result(self, result):
        self.result = result

    def output_file(self):
        pass

    def input_file(self):
        pass

    def exceed(self, previous):
        for i in range(self.number_of_equations):
            ea = self.result[i] - previous[i]
            if ea > self.es:
                return False
        return True
