from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class PlotWindow(QWidget):
    def __int__(self, main_window):
        QWidget.__init__(self)
        loadUi("scenes/plot_window.ui", self)
        self.main_window = main_window
