from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi


class IterativeSteps(QWidget):
    def __int__(self, main_window):
        QWidget.__init__(self, main_window)
        loadUi("scenes/steps_window.ui", self)
        self.main_window = main_window
