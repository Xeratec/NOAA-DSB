#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: minor_frame_test.py
Author: Philip Wiese
Date created: 24.05.2019
Date last modified: 25.05.2019
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

import sys
from pathlib import Path
sys.path.append(str(Path('.').absolute().parent))

from minor_frame import MinorFrame
from bitarray import bitarray

def main():
    rawStream = open("../../NOAA_DSB_MinorFrames.txt").readlines()

    print_zero_frames(rawStream)
    #print_n_frames(rawStream, num=10, skip=166, filter='none', verbose=0)

def print_zero_frames(rawStream, verbose=0):
    # Zero Frames
    zeroFrames = []
    zeroFrames.append(rawStream[167 -1])
    zeroFrames.append(rawStream[441 -1])
    zeroFrames.append(rawStream[762 -1])
    zeroFrames.append(rawStream[1082-1])
    zeroFrames.append(rawStream[1413-1])
    zeroFrames.append(rawStream[1643-1])
    zeroFrames.append(rawStream[1644-1])
    zeroFrames.append(rawStream[1879-1])
    zeroFrames.append(rawStream[2154-1])
    zeroFrames.append(rawStream[2476-1])
    zeroFrames.append(rawStream[2796-1])
    zeroFrames.append(rawStream[3110-1])
    zeroFrames.append(rawStream[3410-1])


    for rawFrame in zeroFrames:
        rawFrame = rawFrame.replace(" ", "")
        rawFrame = rawFrame.replace("\n", "")

        bitStream = ''
        for elem in rawFrame:
            bitStream += bin(int(elem, 16))[2:].zfill(4)

        frame = MinorFrame(bitarray(bitStream))

        if verbose > 0:
            print()
            print("### RAW Frame (HEX) ###")
            print("RAW   :    %s %s" % (len(rawFrame), rawFrame))

        print()
        print(frame.report(verbose))

def print_n_frames(rawStream, num=10, skip=0, verbose=0, filter='none'):
    # Zero Frames
    i = skip
    n = skip+num
    while (i < n and i < len(rawStream)):
        rawStream[i] = rawStream[i].replace(" ", "")
        rawStream[i] = rawStream[i].replace("\n", "")

        bitStream = ''
        for elem in rawStream[i]:
            bitStream += bin(int(elem, 16))[2:].zfill(4)

        frame = MinorFrame(bitarray(bitStream))

        if verbose > 0:
            print()
            print("### RAW Frame (HEX) ###")
            print("RAW   :    %s %s" % (len(rawStream[i]), rawStream[i]))

        if filter == 'parity':
            if not frame.get_parity().parity:
                n += 1
                i += 1
                continue
        elif filter == 'full':
            if not all(frame.get_parity().data):
                n += 1
                i += 1
                continue

        print()
        print(frame.report(verbose))
        i += 1




if __name__ == "__main__":
    main()

