#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: stats_widget.py
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

from typing import List
from PyQt5 import QtCore, QtGui, QtWidgets
import design_stats
from analyzer.major_frame import MajorFrame
from analyzer.minor_frame import MinorFrame


class StatsWidget(QtWidgets.QWidget, design_stats.Ui_Form):
    def __init__(self, Form):
        super(self.__class__, self).__init__()
        self.setupUi(Form)

