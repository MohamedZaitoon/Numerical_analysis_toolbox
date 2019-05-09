from abc import ABC, abstractmethod


class Method(ABC):

    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def set_absolute_error_criteria(self, absolute_error_criteria):
        pass

    @abstractmethod
    def set_max_iterations_criteria(self, max_iterations_criteria):
        pass

    @abstractmethod
    def get_absolute_error(self):
        pass

    @abstractmethod
    def get_iterations(self):
        pass

    @abstractmethod
    def get_error(self):
        pass

    @abstractmethod
    def get_root_value(self):
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
    def set_scale(self, scale):
        pass

    @abstractmethod
    def output_file(self):
        pass
