from abc import ABC, abstractmethod


class Method(ABC):
    @abstractmethod
    def calculate(self, equation, it=50, eps=0.00001):
        pass

    @abstractmethod
    def plot(self, graph):
        pass

    @abstractmethod
    def next_step(self):
        pass

    @abstractmethod
    def prev_step(self):
        pass

    @abstractmethod
    def get_root_values(self):
        pass

    @abstractmethod
    def get_iteration(self):
        pass

    def get_error(self):
        pass

    @abstractmethod
    def output_file(self):
        pass
