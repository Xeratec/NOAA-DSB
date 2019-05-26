#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: major_frame_test.py
Author: Philip Wiese
Date created: 25.05.2019
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

from typing import List

from major_frame import MajorFrame
from minor_frame import MinorFrame


COUNT_THRESHOLD = 100


def main():
    rawStream = open("../../NOAA_DSB_MinorFrames.txt").readlines()

    # Create minor frames from stream
    all_minor_frames: List[MinorFrame] = [MinorFrame(x) for x in rawStream]

    minor_frame_filter: List[MinorFrame] = all_minor_frames

    for i in range(1, len(minor_frame_filter)-1):
        if i >= len(minor_frame_filter)-1: break
        count0 = minor_frame_filter[i-1].get_count().data
        count1 = minor_frame_filter[i].get_count().data
        count2 = minor_frame_filter[i+1].get_count().data

        if abs(count0 - count1) > COUNT_THRESHOLD and abs(count1-count2) > COUNT_THRESHOLD:
            minor_frame_filter.remove(minor_frame_filter[i])

    major_frames: List[MajorFrame] = []
    mf: List[MinorFrame] = []

    count_last = minor_frame_filter[0].get_count().data
    for minor_frame in minor_frame_filter:
        count = minor_frame.get_count().data

        if abs(count - count_last) > COUNT_THRESHOLD:
            if len(mf) > 10:
                major_frames.append(MajorFrame(mf))
                mf.clear()

        count_last = count
        mf.append(minor_frame)

    print("### Unfiltered ###")
    print(major_frames)

    for major_frame in major_frames:
        major_frame.filter('full')

    print()
    print("### Full Filtering ###")
    print(major_frames)

    for major_frame in major_frames:
        major_frame.filter('parity')

    print()
    print("### Parity Check Filtering ###")
    print(major_frames)

    for major_frame in major_frames:
        print(major_frame.report())

    # Select best frame
    top_frame: MajorFrame = major_frames[0]
    for major_frame in major_frames:
        if major_frame.get_score() > top_frame.get_score():
            top_frame = major_frame

if __name__ == "__main__":
    main()

