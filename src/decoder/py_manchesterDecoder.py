#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: py_manchesterDcoder.py
Author: Philip Wiese
Date created: 15.05.2019
Date last modified: 15.05.2019
Python Version: 3

Example:
    Examples can be given using either the ``Example`` or ``Examples``
    sections. Sections support any reStructuredText formatting, including
    literal blocks::

        $ python py_manchesterDecoder.py -f ../../RandomGnuRadioStuff/6_bits_dcblock2.raw  -v 2 -c 1996800 -i 1
        $ python py_manchesterDecoder.py -f ../test/demod_imag.raw  -v 2 -c -1 -i 0

Todo:
    * Perform parity checks
    * Save output
"""


import numpy as np
from bitarray import bitarray
from tqdm import tqdm
from scipy import stats

import sys

CLI_WIDTH = 64

SyncWord = '1110110111100010000' #0100'; %NOAA15 ID last 4 0100
SyncWordInverse = '0001001000011101111' #1011'; %NOAA15 ID

dt = 1 / (8320 * 2)

def str2hex(data):
    """Convert a string to their hex representation"""
    tmp = ''
    for e in range(0, len(data), 2):
        # Grab 2 characters and decode them as their hex values
        tmp += data[e:e + 2].decode('hex_codec')
    return tmp



def usage():
    """Prints help message."""
    print("-f <file>:  Input file (required)")
    print("-c <size>:  Number of bytes to analyze (-1 for everything)")
    print("-i [0,1]:   Specify input format")
    print("              0: Real Values (default)")
    print("              1: Complex Values")
    print("-v <level>: Enable verbose logging. 1-3 (low-high)")
    print("-o <file>:  Output file (default=NOAA_DSB_MinorFrames.txt)")
    sys.exit()


def manchester_decode_nebarnix(bss, bs):
    """Manchester decodes bitstream based on bitstrenght from GRC
    Based on the algorithm of nebarnix
    Source: <http://wiki.nebarnix.com/w/images/e/e0/POES.m>

    :param bss: array. float stream representing bit strength
    :param bs: bitarray. Input bit stream
    :return bsd: bitarray. decoded bitstream
    """

    bsd = bitarray()

    bitThreshold = 0.8
    idx2 = 10
    clockmod = 0
    errx = []

    with tqdm(total=len(bss), ncols=CLI_WIDTH, unit='bit', unit_scale=True) as pbar:
        for idx in range(1,bs.length()-1):
            # If not a bit boundary, see if it should be and we're out of sync
            # But only resync on strong bits
            if ((idx % 2) == clockmod):
                if (bs[idx-1] == bs[idx]):
                    errx.append(idx2)

                    if(abs(bss[idx-1]) > bitThreshold and abs(bss[idx]) > bitThreshold):
                        clockmod = 1-clockmod

            # check for bit boundary, and make decision using the strongest of the two bits.
            if ((idx % 2) != clockmod):
                if (abs(bss[idx]) > abs(bss[idx+1])):
                    if (bs[idx] == 1):
                        bsd.append(0)
                    else:
                        bsd.append(1)
                else:
                    if (bs[idx+1] == 1):
                        bsd.append(1)
                    else:
                        bsd.append(0)
                idx2 = idx2 + 1
            pbar.update(1)

    return bsd


def gen_bitstream(bss):
    """Generate bitstream from strenght array

    :param bss: array. float stream representing bit strength
    :return bs: bitarray. bitstream
    """
    with tqdm(total=len(bss), ncols=CLI_WIDTH, unit='bit', unit_scale=True) as pbar:
        bs = bitarray()
        for c in bss:
            pbar.update(1)
            if c > 0:
                bs.append(1)
            else:
                bs.append(0)

        return bs

def compare_bs(bs1, bs2, perLine=64):
    """Compare two bitarrays and mark differences

    :param bs1: bitarray. bitsream 1
    :param bs2: bitarray. bitstream 2
    :param perLine: integer. number of bits per Line
    """

    length = min(bs1.length(), bs2.length())
    for i in range(0, length, perLine):
        result = '      '
        for b in range(0,perLine):
            if i+b < length:
                if (bs1[i+b] == bs2[i+b]):
                    result += ' '
                else:
                    result += '*'
        if '*' in result:
            print("%04d: %s" % (i/perLine, bs1[i:i + perLine].to01()))
            print(result)


def print_format(bs, perLine):
    """Print bitarray with <perLine> Values per line with line counter

    :param bs: bitarray. bitsream
    :param perLine: integer. number of bits per Line
    """

    for i in range(0, bs.length(), perLine):
        print("%04d: %s" % (i//perLine,bs[i:i+perLine].to01()))


def main():
    """Main code of the programm"""
    bitStreamStrength = []

    # Set values
    filename = ''  # input file
    outputFilename = 'NOAA_DSB_MinorFrames.txt'
    num = -1
    verbose = 0;
    bsFormat = 0;

    # Process Options
    ops = ['-f', '-c', '-v', '-i', '-o']

    while len(sys.argv) > 1:
        op = sys.argv.pop(1)
        if op == '-f':
            filename = sys.argv.pop(1)
        if op == '-c':
            num = int(sys.argv.pop(1))
        if op == '-v':
            verbose = int(sys.argv.pop(1))
        if op == '-i':
            bsFormat = int(sys.argv.pop(1))
        if op == '-o':
            outputFilename = sys.argv.pop(1)
        if op not in ops:
            print("Unknown option:")
            usage()

    # Grab file data
    try:
        filedescriptor = open(filename, "r")# Help
        rawInput = np.fromfile(filedescriptor, dtype=np.float32, count=num)
        filedescriptor.close()

        if bsFormat == 1: # Complex valued bitstream
            bitStreamStrength = rawInput[1::2]
        else:
            bitStreamStrength = rawInput
    except:
        print("Error accessing file:", filename)
        usage()

    RawTime = np.linspace(0, dt * len(bitStreamStrength), len(bitStreamStrength))


    print('[INFO] Size: %d' % len(bitStreamStrength))
    print('[INFO] Duration: %0.2fs' % RawTime[-1])

    # Generate bitstream based on strength
    if verbose > 0: print("[INFO] Generate bitstream")
    bitStream = gen_bitstream(bitStreamStrength)

    # Manchester decode bitstream
    if verbose > 0: print("[INFO] Decode bitstream")
    bitStreamDecoded = manchester_decode_nebarnix(bitStreamStrength, bitStream)

    # For dev purpose
    # to compare Matlab output

    # mbs = bitarray(sio.loadmat('mbs.mat')['bitstream01'][0].tolist())
    # mbsd = bitarray(sio.loadmat('mbsd.mat')['bitstream_manchester01'][0].tolist())
    #
    # print("Compare bitsream:")
    # compare_bs(bitStream, mbs, CLI_WIDTH)
    # print()
    # print("Compeare decoded bitstream:")
    # compare_bs(bitStreamDecoded, mbsd, CLI_WIDTH)
    # print()

    if verbose > 2:
        print("[DEBUG] Raw bitstream:")
        print_format(bitStream, CLI_WIDTH)

        print()
        print("[DEBUG] Decoded bitstream:")
        print_format(bitStreamDecoded, CLI_WIDTH)

    # Search for SyncWord
    idxSyncWord = bitStreamDecoded.search(bitarray(SyncWord))
    idxSyncWordInv = bitStreamDecoded.search(bitarray(SyncWordInverse))


    if verbose >0:
        print("[INFO] Found: %d normal and %d inverted syncword" % (len(idxSyncWord), len(idxSyncWordInv)))
        matchLength = np.sum(np.mod(np.diff(idxSyncWord), 832) == 0) + np.sum(np.mod(np.diff(idxSyncWordInv), 832) == 0)
        print("[INFO] Match length: %d" % matchLength)


    # Extract minor frames at matched syncword locations and invert if necessary
    minorFrames = []

    idxSyncWordAll = []
    idxSyncWordAll.extend(idxSyncWord)
    idxSyncWordAll.extend(idxSyncWordInv)
    idxSyncWordAll.sort()

    # Build minorFrames
    for idx in idxSyncWordAll:
        frame = bitarray(bitStreamDecoded[idx:idx+102])
        if idx in idxSyncWord:
            minorFrames.append(frame)
        if idx in idxSyncWordInv:
            frame.invert()
            minorFrames.append(frame)

    # Detect Spacecraft ID
    spacecrafts = []
    for mf in minorFrames:
        spacecrafts.append(int(mf[16:24].to01(),2))

    if verbose > 1:
        for idx in range(0,len(minorFrames)):
            print()
            print("[INFO] Frame ", idx+1)
            print_format(minorFrames[idx], CLI_WIDTH)
            print("Spacecaft ID: ", spacecrafts[idx])
        print()

    # Most sendt spacecraft id
    spacecraft = stats.mode(spacecrafts)[0][0]

    if spacecraft == 8:
        print("[INFO] ID: %d => NOAA-15" % spacecraft)
    elif spacecraft == 13:
        print("[INFO] ID: %d => NOAA-18" % spacecraft)
    elif spacecraft == 15:
        print("[INFO] ID: %d => NOAA-19" % spacecraft)
    else:
        print("[INFO] ID: %d => UFO!!" % spacecraft)

    # Perform parity checks


if __name__ == "__main__":
    main()
