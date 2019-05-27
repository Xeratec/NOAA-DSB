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

import sys
from pathlib import Path
sys.path.append(str(Path('./gui').absolute()))


import numpy as np
from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar, FigureCanvasQTAgg)
from matplotlib.legend import Legend

from analyzer.major_frame import MajorFrame
from analyzer.major_frame import MEPED

import design_sem

class SEMWidget(QtWidgets.QWidget, design_sem.Ui_Form):


    legend1: Legend = None
    legend2: Legend = None

    meped_canvas1: FigureCanvasQTAgg
    all_data = None

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.meped_canvas1 = FigureCanvas(Figure(figsize=(5, 3)))
        self.gridLayout.addWidget(self.meped_canvas1, 3, 0,1,2)
        self.gridLayout.addWidget(NavigationToolbar(self.meped_canvas1, self), 2,0,1,2)
        self.meped_ax1 = self.meped_canvas1.figure.subplots()
        self.meped_canvas1.figure.subplots_adjust(top=1.0,bottom=0.14,left=0.06,right=0.995,hspace=0.2,wspace=0.2)

        self.meped_canvas2 = FigureCanvas(Figure(figsize=(5, 3)))
        self.gridLayout.addWidget(self.meped_canvas2, 5, 0,1,2)
        self.gridLayout.addWidget(NavigationToolbar(self.meped_canvas2, self), 4, 0, 1, 2)
        self.meped_ax2 = self.meped_canvas2.figure.subplots()
        self.meped_canvas2.figure.subplots_adjust(top=1.0,bottom=0.14,left=0.06,right=0.995,hspace=0.2,wspace=0.2)

    def onSourceChange(self):
        self.draw_data()

    def set_data(self,major_frames: List[MajorFrame]):
        self.all_data = MEPED()

        for major_frame in major_frames:
            meped = major_frame.get_sem_meped()
            self.all_data.MEPED_0P1 += meped.MEPED_0P1
            self.all_data.MEPED_0P2 += meped.MEPED_0P2
            self.all_data.MEPED_0P3 += meped.MEPED_0P3
            self.all_data.MEPED_0P4 += meped.MEPED_0P4
            self.all_data.MEPED_0P5 += meped.MEPED_0P5
            self.all_data.MEPED_0P6 += meped.MEPED_0P6

            self.all_data.MEPED_0E1 += meped.MEPED_0E1
            self.all_data.MEPED_0E2 += meped.MEPED_0E2
            self.all_data.MEPED_0E3 += meped.MEPED_0E3

            self.all_data.MEPED_9P1 += meped.MEPED_9P1
            self.all_data.MEPED_9P2 += meped.MEPED_9P2
            self.all_data.MEPED_9P3 += meped.MEPED_9P3
            self.all_data.MEPED_9P4 += meped.MEPED_9P4
            self.all_data.MEPED_9P5 += meped.MEPED_9P5
            self.all_data.MEPED_9P6 += meped.MEPED_9P6

            self.all_data.MEPED_9E1 = meped.MEPED_9E1
            self.all_data.MEPED_9E2 = meped.MEPED_9E2
            self.all_data.MEPED_9E3 = meped.MEPED_9E3

            self.all_data.MEPED_P6 = meped.MEPED_P6
            self.all_data.MEPED_P7 = meped.MEPED_P7
            self.all_data.MEPED_P8 = meped.MEPED_P8
            self.all_data.MEPED_P9 = meped.MEPED_P9


    def draw_data(self):
        self.meped_ax1.clear()
        self.meped_ax2.clear()

        if self.cbSource.currentIndex() == 0:
            self.meped_ax1.set_title("Proton Telescope 0 Degrees")
            l_MEPED_0P1 = np.arange(0, len(self.all_data.MEPED_0P1))
            l_MEPED_0P2 = np.arange(0, len(self.all_data.MEPED_0P2))
            l_MEPED_0P3 = np.arange(0, len(self.all_data.MEPED_0P3))
            l_MEPED_0P4 = np.arange(0, len(self.all_data.MEPED_0P4))
            l_MEPED_0P5 = np.arange(0, len(self.all_data.MEPED_0P5))
            l_MEPED_0P6 = np.arange(0, len(self.all_data.MEPED_0P6))

            self.meped_ax1.plot(l_MEPED_0P1, self.all_data.MEPED_0P1, label="30-80 keV")
            self.meped_ax1.plot(l_MEPED_0P2, self.all_data.MEPED_0P2, label="80-250 keV")
            self.meped_ax1.plot(l_MEPED_0P3, self.all_data.MEPED_0P3, label="250-800 keV")
            self.meped_ax1.plot(l_MEPED_0P4, self.all_data.MEPED_0P4, label="800-2500 keV")
            self.meped_ax1.plot(l_MEPED_0P5, self.all_data.MEPED_0P5, label="2500-7000 keV")
            self.meped_ax1.plot(l_MEPED_0P6, self.all_data.MEPED_0P6, label="> 7000 keV")

            self.meped_ax2.set_title("Proton Telescope 90 Degrees")
            l_MEPED_9P1 = np.arange(0, len(self.all_data.MEPED_9P1))
            l_MEPED_9P2 = np.arange(0, len(self.all_data.MEPED_9P2))
            l_MEPED_9P3 = np.arange(0, len(self.all_data.MEPED_9P3))
            l_MEPED_9P4 = np.arange(0, len(self.all_data.MEPED_9P4))
            l_MEPED_9P5 = np.arange(0, len(self.all_data.MEPED_9P5))
            l_MEPED_9P6 = np.arange(0, len(self.all_data.MEPED_9P6))

            self.meped_ax2.plot(l_MEPED_9P1, self.all_data.MEPED_9P1, label="30-80 keV")
            self.meped_ax2.plot(l_MEPED_9P2, self.all_data.MEPED_9P2, label="80-250 keV")
            self.meped_ax2.plot(l_MEPED_9P3, self.all_data.MEPED_9P3, label="250-800 keV")
            self.meped_ax2.plot(l_MEPED_9P4, self.all_data.MEPED_9P4, label="800-2500 keV")
            self.meped_ax2.plot(l_MEPED_9P5, self.all_data.MEPED_9P5, label="2500-7000 keV")
            self.meped_ax2.plot(l_MEPED_9P6, self.all_data.MEPED_9P6, label="> 7000 keV")

        if self.cbSource.currentIndex() == 1:
            self.meped_ax1.set_title("Electron Telescope 0 Degrees")
            l_meped_0E1 = np.arange(0, len(self.all_data.MEPED_0E1))
            l_meped_0E2 = np.arange(0, len(self.all_data.MEPED_0E2))
            l_meped_0E3 = np.arange(0, len(self.all_data.MEPED_0E3))

            self.meped_ax1.plot(l_meped_0E1, self.all_data.MEPED_0E1, label="≥ 30 keV")
            self.meped_ax1.plot(l_meped_0E2, self.all_data.MEPED_0E2, label="≥ 100 keV")
            self.meped_ax1.plot(l_meped_0E3, self.all_data.MEPED_0E3, label="≥ 300 keV")

            self.meped_ax2.set_title("Electron Telescope 90 Degrees")
            l_meped_9E1 = np.arange(0, len(self.all_data.MEPED_9E1))
            l_meped_9E2 = np.arange(0, len(self.all_data.MEPED_9E2))
            l_meped_9E3 = np.arange(0, len(self.all_data.MEPED_9E3))
        
            self.meped_ax2.plot(l_meped_9E1, self.all_data.MEPED_9E1, label="≥ 30 keV")
            self.meped_ax2.plot(l_meped_9E2, self.all_data.MEPED_9E2, label="≥ 100 keV")
            self.meped_ax2.plot(l_meped_9E3, self.all_data.MEPED_9E3, label="≥ 300 keV")

        if self.cbSource.currentIndex() == 2:
            self.meped_ax1.set_title("Proton Omnidirectional")
            l_meped_P6 = np.arange(0, len(self.all_data.MEPED_P6))
            l_meped_P7 = np.arange(0, len(self.all_data.MEPED_P7))
            l_meped_P8 = np.arange(0, 2*len(self.all_data.MEPED_P8),2)
            l_meped_P9 = np.arange(0, 2*len(self.all_data.MEPED_P9),2)
            self.meped_ax2.set_title("Proton Omnidirectional")
            self.meped_ax1.plot(l_meped_P6, self.all_data.MEPED_P6, label="≥ 16 MeV")
            self.meped_ax1.plot(l_meped_P7, self.all_data.MEPED_P7, label="≥ 35 MeV")
            self.meped_ax2.plot(l_meped_P8, self.all_data.MEPED_P8, label="≥ 70 MeV")
            self.meped_ax2.plot(l_meped_P9, self.all_data.MEPED_P9, label="≥ 140 MeV")

        if self.legend1:
            self.legend1.remove()
        self.legend1 = self.meped_ax1.figure.legend(fontsize=7)
        if self.legend2:
            self.legend2.remove()
        self.legend2 = self.meped_ax2.figure.legend(fontsize=8)
        self.meped_ax1.figure.canvas.draw()
        self.meped_ax2.figure.canvas.draw()