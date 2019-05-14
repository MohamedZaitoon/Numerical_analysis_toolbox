from abc import ABC, abstractmethod


class Interface(ABC):

    @abstractmethod
    def set_coefficients(self, coefficients, number_of_equations):
        pass

    @abstractmethod
    def set_constants(self, constants):
        pass

    @abstractmethod
    def set_result(self, result):
        pass

    @abstractmethod
    def calculate(self):
        pass

    @abstractmethod
    def get_solution(self):
        pass

    @abstractmethod
    def get_system_type(self):
        pass

    @abstractmethod
    def output_file(self):
        pass

    @abstractmethod
    def input_file(self):
        pass
