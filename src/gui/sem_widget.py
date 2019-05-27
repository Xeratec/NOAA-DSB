#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: sem_widget.py
Author: Philip Wiese
Date created: 27.05.2019
Date last modified: 27.05.2019
Python Version: 3

License:
Copyright (C) 2019  Philip Wiese

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Contact:
philip.wiese@maketec.ch
"""

import time

import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
        FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


import design_sem


class SEMWidget(QtWidgets.QWidget, design_sem.Ui_Form):
    def __init__(self, Form):
        super(self.__class__, self).__init__()
        self.setupUi(Form)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.gridLayout.addWidget(static_canvas)
        # self.addToolBar(NavigationToolbar(static_canvas, self))

        dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.gridLayout.addWidget(dynamic_canvas)
        # self.addToolBar(QtCore.Qt.BottomToolBarArea,NavigationToolbar(dynamic_canvas, self))

        self._static_ax = static_canvas.figure.subplots()
        t = np.linspace(0, 10, 501)
        self._static_ax.plot(t, np.tan(t), ".")

        self._dynamic_ax = dynamic_canvas.figure.subplots()
        self._timer = dynamic_canvas.new_timer(
            100, [(self._update_canvas, (), {})])
        self._timer.start()

    def _update_canvas(self):
        self._dynamic_ax.clear()
        t = np.linspace(0, 10, 101)
        # Shift the sinusoid as a function of time.
        self._dynamic_ax.plot(t, np.sin(t + time.time()))
        self._dynamic_ax.figure.canvas.draw()
