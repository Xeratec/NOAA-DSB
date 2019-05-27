#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: noaa_analyze.py
Author: Philip Wiese
Date created: 17.05.2019
Date last modified: 23.05.2019
Python Version: 3

Example:
    $ python analyzer/noaa_analyzer.py -f NOAA_DSB_MinorFrames.txt -v 2

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
from typing import List

from major_frame import MajorFrame
from minor_frame import MinorFrame

def usage(copyright = 0):
    """Prints help message."""
    if copyright:
        print("Copyright (C) 2019  Philip Wiese")
        print("This program comes with ABSOLUTELY NO WARRANTY.")
        print("This is free software, and you are welcome to redistribute it")
        print("under certain conditions.)")
        print()
    print("Usage:")
    print("     -f <file>:  Input file (required)")
    print("     -v <level>: Set logging level")
    print("                   0: No output")
    print("                   1: Info (default)")
    print("                   2: Debug")
    print("                   3: All")
    print("     -d <filter> Specify filter method")
    print("                   'unfiltered': No filtering (default)")
    print("                   'parity'    : Filter frames with last parity bit wrong")
    print("                   'full'      : Filter frames with at least on wrong parity bit")
    print("     -o <file>:  Output file (default=NOAA_DSB_Frames.txt)")
    sys.exit()

def main():
    # Set values
    filename = ''  # input file
    outputFilename = 'NOAA_DSB_Frames.txt'
    verbose = 1
    filter_method = 'unfiltered'

    # Process Options
    ops = ['-f', '-v', '-o', 'd']

    if len(sys.argv) == 1:
        usage(copyright=1)

    while len(sys.argv) > 1:
        op = sys.argv.pop(1)
        if op == '-f':
            filename = sys.argv.pop(1)
        if op == '-d':
            filter_method = sys.argv.pop(1)
        if op == '-v':
            verbose = int(sys.argv.pop(1))
        if op == '-o':
            outputFilename = sys.argv.pop(1)
        if op not in ops:
            print("Unknown option:")
            usage(copyright=1)

    # Grab file data
    try:
        rawStream = open(filename).readlines()
    except:
        print("[ERROR] Error accessing file:", filename)
        usage()

    # Create minor frames from stream
    all_minor_frames: List[MinorFrame] = [MinorFrame(x) for x in rawStream]

    minor_frame_filter = filter_before_next(all_minor_frames, 10, 3)
    minor_frame_filter = filter_mf_count(minor_frame_filter.copy(), 1)

    major_frames: List[MajorFrame] = []
    mf: List[MinorFrame] = []

    # Slice minor frames based on major frame count (id) number
    # Create major frames
    count_last = minor_frame_filter[0].get_major_count().data
    for minor_frame in minor_frame_filter:
        count = minor_frame.get_major_count().data

        if abs(count - count_last) > 0:
            if len(mf) > 20:
                major_frames.append(MajorFrame(mf))
                mf.clear()

        count_last = count
        mf.append(minor_frame)

    # Last Frame
    if len(mf) > 20:
        major_frames.append(MajorFrame(mf))

    try:
        outputFiledescriptor = open(outputFilename, "w")
    except:
        print("Error accessing file:", outputFilename)
        usage()

    if verbose > 0:
        print("Saving output to:", outputFilename)

    # Demonstrate and test filter capability
    if filter_method == 'parity':
        if verbose > 0:
            print("### Parity Check Filtering ###")
        outputFiledescriptor.writelines("### Parity Check Filtering ###\n")
        for major_frame in major_frames:
            major_frame.filter('parity')

    elif filter_method == 'parity':
        if verbose > 0:
            print("### Full Filtering ###")
        outputFiledescriptor.writelines("### Full Filtering ###\n")
    for major_frame in major_frames:
        major_frame.filter('full')

    else:
        if verbose > 0:
            print("### Unfiltered ###")
        outputFiledescriptor.writelines("### Unfiltered ###\n")
        for major_frame in major_frames:
            major_frame.filter('unfilterd')

    if verbose > 1:
        print(major_frames)

    outputFiledescriptor.writelines(str(major_frames))

    for major_frame in major_frames:
        outputFiledescriptor.writelines("\n###########################################################################\n")
        outputFiledescriptor.writelines(major_frame.report(1))
        if verbose > 2:
            print("###########################################################################")
            print(major_frame.report(1))


def filter_before_next(minor_frame_filter: List[MinorFrame], threshold=20, iterations = 2):
    # Remove minor frames with to high count (id) number
    for n in range(iterations):
        for i in range(1, len(minor_frame_filter) - 1):
            if i >= len(minor_frame_filter) - 1: break

            count0 = minor_frame_filter[i - 1].get_count().data
            count1 = minor_frame_filter[i].get_count().data
            count2 = minor_frame_filter[i + 1].get_count().data

            if abs(count0 - count1) > threshold and abs(count1 - count2) > threshold:
                minor_frame_filter.remove(minor_frame_filter[i])

    return minor_frame_filter


def filter_mf_count(minor_frames: List[MinorFrame], iterations = 2):

    for n in range(iterations):
        minor_frame_filter = minor_frames.copy()

        for i in range(0, len(minor_frame_filter)-2):

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


if __name__ == "__main__":
    main()

