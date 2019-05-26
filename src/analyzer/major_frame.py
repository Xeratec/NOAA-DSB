#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: major_frame.py
Author: Philip Wiese
Date created: 23.05.2019
Date last modified: 23.05.2019
Python Version: 3

Object oriented major frame implementation

The TIP format is based on a major frame which contains 320 minor frames.
The Major Frame consists of 320 0.1 second Minor Frames

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

from minor_frame import MinorFrame
from typing import List


class MajorFrame:
    # 1 Major Frame is
    # 320 minor frames

    minor_frames: List[MinorFrame] = [None for x in range(320)]

    # Minor Frame Count
    #   000 Major Frame 0; 111=Major Frame 7; MSB first; Counter
    #   incremented every 320 minor frames
    count = None

    # Time code (Minor Frame 0 only)
    # The data inserted is referenced to the beginning of the first bit
    # of the minor frame sync word of minor frame 0 within ∀ millisecond.
    time_code = None

    # Digital "B" Subcom-1
    #   A Subcommutation of Discrete Inputs collected to form 8 bit words. 256 Discrete
    #   Inputs (32 words) can be accommodated. It takes 32 frames to sample all inputs once
    #   (sampling rate=once/3.2 sec). A Major Frame contains 10 complete Digital “B”
    #   subcommutated frames.
    digital_b_subcom_1 = None

    # Analog Subcom-1 (32 sec)
    #   A subcommutation of up to 191 analog points sampled once every 32 seconds plus
    #   64 analog points sampled twice every 32 seconds (once every 16 seconds).
    #   Bit 1 of each word represents 2560 mV, while Bit 8 represents 20 mV.
    analog_subcom_1_32 = None

    # Analog Subcom-1 (16 sec)
    #   This subcommutation is controlled by a PROM located in the TIP and contains
    #   160 word locations with 128 analog channels sampled once every 16 seconds.
    analog_subcom_1_16 = None

    # Analog Subcom-1 (1 sec)
    #   This subcommutation is controlled by a PROM in the TIP and contains 10
    #   analog channels sampled once every 1 second. Word 0 of this subcom is
    #   filled with data from an analog point selected by command. The selected
    #   analog point may be one of the 512 analog points available to the TIP.
    #   Bit on of each word represents 2560 mV while Bit 8 represents 20 mV.
    analog_subcom_1_1 = None

    # Digital "B" Subcom-2
    #   The subcommutation of discrete inputs collected to form 8 Bit words.
    #   256 discrete inputs (32 words) can be accommodated. It takes 32 minor frames
    #   to sample all inputs once (sampling rate=once/3.2 sec). A Major Frame contains
    #   10 complete Digital “B” subcommutated frames.
    #   64 of these bit locations corresponding to TIP minor frames 24-31 form the
    #   XSU Digital “A” data. The XSU generates an 8 word subcom which is read out
    #   at the rate of one word per minor frame. The XSU subcom is synchronized with
    #   its word 1 in minor frame 24.
    digital_b_subcom_2 = None

    # Analog Subcom-2 (16)
    #   This subcommutation is controlled by a PROM located in the TIP and contains 160
    #   words locations with 128 analog channels sampled once every 16 seconds.
    #   The remaining 32 word locations contain data from the Solar Array Telemetry
    #   Commutator Unit (SATCU). The SATCU receives inputs from 16 sources on the
    #   solar array, commutates them and presents this stream and presents it in the last 32
    #   word locations. The 32 words represent two successive passes through the SATCU subcom.
    analog_subcom_2_16 = None

    # HIRS/
    #   HIRS/3, HIRS/4 on NOAA-N (18), -N’ (19)
    hirs = None

    # SEM
    sem = None

    # DCS-2
    dcs_2 = None

    # SBUF/2
    sbuv_2 = None

    REFERENCE_FRAME = 0

    filter_num = 0
    filter_method = 'None'
    saved_minor_frames = None

    def __init__(self, __minor_frames):

        """
        Construction for MajorFrame class
        :type __minor_frames: List[MinorFrame]
        :param __minor_frames:  minor frames
        """

        if __minor_frames is None: raise ValueError

        self.minor_frames: List[MinorFrame] = [None for x in range(320)]
        for i in range(len(__minor_frames)):
            count = __minor_frames[i].get_count().data

            if count < 320:
                self.minor_frames[count] = __minor_frames[i]

        self.saved_minor_frames = self.minor_frames.copy()

    def filter(self, method='parity'):
        """
        Filter minor frames based on parity check
        :param method: string.  'parity':   Remove minor frames with last parity bit invalid, indicating
                                            the possibility of wrong parity bits
                                'full':     Remove all minor frames with at least one wring parity check
        :return: int. number of removed minor frames
        """
        self.filter_num = 0

        for i in range(len(self.minor_frames)):
            if not self.saved_minor_frames[i]: continue

            frame = self.saved_minor_frames[i]
            self.minor_frames[i] = frame
            if method == 'parity':
                if not frame.get_parity().parity:
                    self.filter_num += 1
                    self.minor_frames[i] = None
            elif method == 'full':
                if not all(frame.get_parity().data):
                    self.filter_num += 1
                    self.minor_frames[i] = None

        self.filter_method = method

        return self.filter_num

    # TODO
    def get_filter_stats(self):
        return (self.filter_method, self.filter_num)

    def get_minor_frame_count(self):
        return sum(x is not None for x in self.saved_minor_frames)

    def get_score(self):
        n = self.get_minor_frame_count()
        e = self.filter_num
        p = 100-100/n*e if n!=0 else 0
        return p

    def get_spacraft(self):
        """
        :return: string. spacecraft name
        """
        if not self.minor_frames[self.REFERENCE_FRAME]: return False
        return self.minor_frames[self.REFERENCE_FRAME].get_spacraft().data


    def get_count(self):
        """
        :return: int. Major frame number
        """
        if not self.minor_frames[self.REFERENCE_FRAME]: return False
        return self.minor_frames[self.REFERENCE_FRAME].get_status().data.major_frame_count

    def get_timestamp(self):
        """
        :return datetime. Day of the year and UTC spacecraft time
        """
        if not self.minor_frames[0]: return False
        if not self.minor_frames[0].get_timestamp(): return False
        return self.minor_frames[0].get_timestamp().data



    # SEM-2 data accumulation and transfer are synchronized to the spacecraft's 32 second Major
    # Frame. The Major Frame consists of 320 0.1 second Minor Frames, and SEM-2 is assigned two
    # Digital A data words (20 and 21) per Minor Frame.

    # MEPED Digital A data consists of six directional proton measurements and three directional
    # electron measurements for each of two directions of incidence (0 and 90 degrees) and four omni-
    # directional proton measurements.

    # TED Digital A data consists of a 0.05 to 1 keV partial energy flux measurement, a 1 to 20 keV
    # partial energy flux measurement, maximum differential energy fluxes, four-point differential
    # energy spectra and background measurements for electrons and protons, each at two angles of
    # incidence (0 and 30 degrees).
    def get_sem(self):

        MEPED_0P1 = []
        MEPED_0P2 = []
        MEPED_0P3 = []
        MEPED_0P4 = []
        MEPED_0P5 = []
        MEPED_0P6 = []

        MEPED_0E1 = []
        MEPED_0E2 = []
        MEPED_0E3 = []

        MEPED_9P1 = []
        MEPED_9P2 = []
        MEPED_9P3 = []
        MEPED_9P4 = []
        MEPED_9P5 = []
        MEPED_9P6 = []

        MEPED_9E1 = []
        MEPED_9E2 = []
        MEPED_9E3 = []

        MEPED_P6 = []
        MEPED_P7 = []
        MEPED_P8 = []
        MEPED_P9 = []

        return NotImplemented


    def get_hirs(self):
        """
        :return parity: int. Validity of information
        :return data: Not yet Impemented
        """
        return NotImplemented

    def __str__(self):
        return self.report(0)

    def __str_debug(self, msg, desc=""):
        return "%s: %s" % (desc, msg)


    def __repr__(self):
        if self.filter_method == 'None':
            return "\nMajorFrame Count %d, #MF %3d, #Err %3d" % (
            self.get_count(), self.get_minor_frame_count(), self.get_minor_frame_count())

        else:
            return "\nMajorFrame Count %d, #MF %3d, #Err %3d, Score %2.2f%%" % (
            self.get_count(), self.get_minor_frame_count(), self.get_minor_frame_count(), self.get_score())

    def report(self, verbose=0):
        s = ""
        s += '\n' + self.__str_debug(self.get_spacraft(),   "ID   ")
        s += '\n' + self.__str_debug(self.get_count(),      "Count")
        s += '\n' + self.__str_debug(self.get_timestamp(),  "Time ")
        s += '\n' + self.__str_debug(self.get_sem(),        "SEM  ")
        # s += '\n' + self.__str_debug(self.get_hirs(),     "HIRS    ")

        return s
