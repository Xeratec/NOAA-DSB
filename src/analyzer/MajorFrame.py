#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: MajorFrame.py
Author: Philip Wiese
Date created: 23.05.2019
Date last modified: 23.05.2019
Python Version: 3

Object oriented major frame implementation

The TIP format is based on a major frame which contains 320 minor frames.
The Major Frame consists of 320 0.1 second Minor Frames
"""

import MinorFrame

class MajorFrame:
    timestamp = None
    count = None
    spacecraft_id = None
    minor_frames = [MinorFrame() for i in range(320)]


    def __init__(self):
        return


