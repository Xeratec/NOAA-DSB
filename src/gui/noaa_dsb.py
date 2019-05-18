#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: noaa_dsb.py
Author: Philip Wiese
Date created: 17.05.2019
Date last modified: 17.05.2019
Python Version: 3

Example:
    $ python
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

from design import design_main
from design import design_stats

class ExampleApp(QtWidgets.QMainWindow, design_main.Ui_MainWindow):
    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        ui = design_stats.Ui_Form()
        ui.setupUi(self.wSEM)


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function    app.exec_()