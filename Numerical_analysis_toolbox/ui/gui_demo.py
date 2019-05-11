# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\firstdemo.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(683, 356)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 171, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.methods = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.methods.setObjectName("methods")
        self.methods.addItem("")
        self.methods.addItem("")
        self.methods.addItem("")
        self.methods.addItem("")
        self.methods.addItem("")
        self.methods.addItem("")
        self.methods.addItem("")
        self.verticalLayout.addWidget(self.methods)
        self.select = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.select.setObjectName("select")
        self.verticalLayout.addWidget(self.select)
        self.nextButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.nextButton.setObjectName("next")
        self.verticalLayout.addWidget(self.nextButton)
        self.prevButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.prevButton.setObjectName("prev")
        self.verticalLayout.addWidget(self.prevButton)
        self.saveButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.saveButton.setObjectName("save")
        self.verticalLayout.addWidget(self.saveButton)
        self.equation = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.equation.setObjectName("equation")
        self.verticalLayout.addWidget(self.equation)
        self.plot = QtWidgets.QWidget(self.centralwidget)
        self.plot.setGeometry(QtCore.QRect(329, -1, 351, 331))
        self.plot.setObjectName("plot")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.methods.setItemText(0, _translate("MainWindow", "Bisection"))
        self.methods.setItemText(1, _translate("MainWindow", "False-Positon"))
        self.methods.setItemText(2, _translate("MainWindow", "Fixed Point"))
        self.methods.setItemText(3, _translate("MainWindow", "Newton-Raphson"))
        self.methods.setItemText(4, _translate("MainWindow", "Secant"))
        self.methods.setItemText(5, _translate("MainWindow", "Birge-Vieta"))
        self.methods.setItemText(6, _translate("MainWindow", "General algorithm"))
        self.select.setText(_translate("MainWindow", "Select"))
        self.nextButton.setText(_translate("MainWindow", "Next>>"))
        self.prevButton.setText(_translate("MainWindow", "<<Prev"))
        self.saveButton.setText(_translate("MainWindow", "save"))


