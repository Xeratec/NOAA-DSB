#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: telemetry.py
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
from typing import ClassVar, List

from PyQt5 import QtCore, QtGui, QtWidgets

from analyzer.major_frame import MajorFrame
from analyzer.minor_frame import MinorFrame


from noaa_dsb import NOAA_DSB


class Telemetry():
    main: ClassVar[NOAA_DSB] = None
    wStats: ClassVar[QtWidgets.QWidget] = None
    wSEM: ClassVar[QtWidgets.QWidget] = None

    major_frames: List[MajorFrame] = None

    COUNT_THRESHOLD = 100

    def __init__(self, widgetStats: QtWidgets.QWidget, widgetSEM: QtWidgets.QWidget, mainWindow: NOAA_DSB):
        self.main = mainWindow
        self.wStats = widgetStats
        self.wSEM = widgetSEM

        self.main.lFrameMajorFrameNum.setText(str(0))

    def load_file(self, filenpath: str):
        """
        Load minor frames from file and generate major frames
        :rtype: str
        :param filenpath: Filepath to file with minor frames
        """

        # Reset
        self.main.cbFrameMajorFrame.clear()
        self.main.cbFrameMinorFrame.clear()

        # Progress bar in GUI
        progress = self.main.bpAnalyzer
        progress.setValue(0)

        self.main.append_output("Process %s\n" % filenpath)
        self.main.status_text.setText("Process %s" % filenpath)


        rawStream = open(filenpath).readlines()

        # Create minor frames from stream
        all_minor_frames: List[MinorFrame] = [MinorFrame(x) for x in rawStream]

        progress.setMaximum(2 * len(all_minor_frames))

        # Filter frames based on minor frame count number
        minor_frame_filter = self.filter_before_next(all_minor_frames, progress, 10, 3)
        # Filter frames based on major frame count number
        minor_frame_filter = self.filter_mf_count(minor_frame_filter.copy(), progress, 1)

        # Slice frames into major frames based on major frame count number
        self.major_frames: List[MajorFrame] = []
        mf: List[MinorFrame] = []

        count_last = minor_frame_filter[0].get_major_count().data
        for minor_frame in minor_frame_filter:
            count = minor_frame.get_major_count().data

            if abs(count - count_last) > 0:
                if len(mf) > 20:
                    self.major_frames.append(MajorFrame(mf))
                    mf.clear()

            count_last = count
            mf.append(minor_frame)

        # Last Frame
        if len(mf) > 20:
            self.major_frames.append(MajorFrame(mf))

        progress.setValue(progress.maximum())

        filter_method = 'unfiltered'
        if self.main.analyze_filter == 1:
            filter_method = 'parity'
        elif self.main.analyze_filter == 2:
            filter_method = 'full'

        for major_frame in self.major_frames:
            major_frame.filter(filter_method)

            # Remove empty frames due to filtering
            if major_frame.get_minor_frame_count() == major_frame.get_filter_stats()[1]:
                self.major_frames.remove(major_frame)

        # Show result in console
        self.main.append_output(str(self.major_frames[0].get_filter_stats()[0])+'\n')
        self.main.append_output(str(self.major_frames)+'\n')

        self.main.status_text.setText("Found %d major frames" % len(self.major_frames))

        # Set major frame number and Spacecraft ID in GUI
        self.main.lFrameMajorFrameNum.setText(str(len(self.major_frames)))
        self.main.lFrameSpacecraftID.setText(str(self.major_frames[0].get_spacraft()))

        for major_frame in self.major_frames:
            self.main.cbFrameMajorFrame.addItem(str(major_frame.get_count()))

        # Switch to Telemetry - Statistics Tab
        self.main.twCentral.setCurrentIndex(1)
        self.main.twTelemetry.setCurrentIndex(0)

    def filter_mf_count(self, minor_frames: List[MinorFrame], progress: QtWidgets.QProgressBar, iterations: int = 2) -> List[MinorFrame]:
        """
        Filter minor frames based on major frame count number
        This function removes frames with changig major frame count number
        :param minor_frames: List of minor frames
        :param progress: Progressbar to show status
        :param iterations: Number of iterations to run filter
        :return: List of filtered minor frames
        """
        for n in range(iterations):
            minor_frame_filter = minor_frames.copy()

            for i in range(0, len(minor_frame_filter)-2):

                progress.setValue(progress.value() + 1)

                before1 = minor_frame_filter[i-1]
                before2 = minor_frame_filter[i-2]
                current = minor_frame_filter[i]

                before1_mf_count = before1.get_status().data.major_frame_count
                before2_mf_count = before2.get_status().data.major_frame_count
                current_mf_count = current.get_status().data.major_frame_count

                if current.get_count().data == 0:
                    continue

                if before1_mf_count == before2_mf_count and before1_mf_count != current_mf_count:
                    minor_frames.remove(current)
                    continue

        return minor_frames

    def filter_before_next(self, minor_frame_filter: List[MinorFrame], progress: QtWidgets.QProgressBar, threshold: int = 20, iterations: int = 2) -> List[MinorFrame]:
        """
        Filter minor frame based on minor frame count number
        This function removes frames with runaway minor frame count numbers
        :param minor_frame_filter: List of minor frames
        :param progress: Progressbar to show status
        :param threshold: Minor frame count number threshold for removing frames
        :param iterations: Number of iterations to run filter
        :return: List of filtered minor frames
        """
        for n in range(iterations):
            for i in range(1, len(minor_frame_filter) - 1):
                if i >= len(minor_frame_filter) - 1: break

                progress.setValue(progress.value() + 1)

                count0 = minor_frame_filter[i - 1].get_count().data
                count1 = minor_frame_filter[i].get_count().data
                count2 = minor_frame_filter[i + 1].get_count().data

                if abs(count0 - count1) > threshold and abs(count1 - count2) > threshold:
                    minor_frame_filter.remove(minor_frame_filter[i])

        return minor_frame_filter

    def update_major_frame_infos(self):
        if self.main.cbFrameMajorFrame.currentText().isnumeric():
            # Delete all Minor Frames
            self.main.cbFrameMinorFrame.clear()

            # Add new minor frames
            for minor_frame in self.major_frames[self.main.cbFrameMajorFrame.currentIndex()].minor_frames:
                if not minor_frame:
                    continue
                self.main.cbFrameMinorFrame.addItem(str(minor_frame.get_count().data))

            major_frame = self.major_frames[self.main.cbFrameMajorFrame.currentIndex()]
            # Display timestamp
            timestamp = major_frame.get_timestamp()
            self.main.lFrameTimestamp.setText(str(timestamp))

            # Display total number of frames
            frames = major_frame.get_minor_frame_count()
            self.main.lFrameFrames.setText(str(frames))

            # Display number of filtered frames
            filter_num = major_frame.get_filter_stats()[1]
            self.main.lFrameFiltered.setText(str(filter_num))

            # Display score
            score = major_frame.get_score()
            self.main.lFrameScore.setText("%2.2f%%" % score)

    def update_minor_frame_infos(self):
        if self.main.cbFrameMinorFrame.currentText().isnumeric():
            minor_frame = self.major_frames[self.main.cbFrameMajorFrame.currentIndex()]\
                .minor_frames[int(self.main.cbFrameMinorFrame.currentText())]
            self.main.textFrame.setPlainText(minor_frame.report(self.main.analyze_log_level))




