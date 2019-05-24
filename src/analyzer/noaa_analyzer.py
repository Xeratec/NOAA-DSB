#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: noaa_analyze.py
Author: Philip Wiese
Date created: 17.05.2019
Date last modified: 23.05.2019
Python Version: 3

Example:
    $ python noaa_decode.py -f ../../RandomGnuRadioStuff/6_bits_dcblock2.raw -v 1 -i 1
"""
WORD_LENGTH = 8
SEM_BYTE_1 = 20
SEM_BYTE_2 = 21

def main():
    return True

def decodeTimeStamp(majorFrame):
    """
    Decodes Timestamp from one major frame

    :param majorFrame: array[bitarray]. array of minorframes saved as bittarrays
    :return time: Date.
    """
    return

def decodeMEPED(majorFrame, time):
    """
    Decodes MEPED data from one major frame
    Based on the algorithm of nebarnix
    Source: <https://github.com/nebarnix/PDT-TelemetryExplorer/blob/master/sem.cpp

    :param majorFrame: array[bitarray]. array of minorframes saved as bittarrays
    :param time: Date. Time of majorframe
    :return meped: array. decoded meped data

    Further Information:
    MEPED Digital A data consists of six directional proton measurements
    and three directional electron measurements for each of two directions
    of incidence (0 and 90 degrees) and four omni-directional proton
    measurements. All but the two highest energy omni-directional proton
    measurements are read out every two seconds. The two highest energy
    omnidirectional proton measurements are read out every four seconds.
    The MEPED Digital A data and readout rates are summarized in Table 4.3.4.2-2.
    """

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


    for frame in majorFrame:
        return





if __name__ == "__main__":
    main()