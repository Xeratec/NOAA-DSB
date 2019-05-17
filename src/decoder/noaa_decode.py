#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
File name: noaa_decode.py
Author: Philip Wiese
Date created: 15.05.2019
Date last modified: 17.05.2019
Python Version: 3

Example:
    $ python noaa_decode.py -f ../../RandomGnuRadioStuff/6_bits_dcblock2.raw -v 1 -i 1
    $ python noaa_decode.py -f ../test/demod_imag.raw -v 2 -o ../test/NOAA-18.txt
"""


import numpy as np
from bitarray import bitarray
from tqdm import tqdm
from scipy import stats
import sys

CLI_WIDTH = 64

SyncWord = bitarray('1110110111100010000')
dt = 1 / (8320 * 2)

def usage():
    """Prints help message."""
    print("Usage:")
    print("     -f <file>:  Input file (required)")
    print("     -c <size>:  Number of bytes to analyze (-1 for everything)")
    print("     -i [0,1]:   Specify input format")
    print("                   0: Real Values (default)")
    print("                   1: Complex Values")
    print("     -v <level>: Enable verbose logging. 0-3 (low-high)")
    print("     -o <file>:  Output file (default=NOAA_DSB_MinorFrames.txt)")
    sys.exit()


def manchester_decode_nebarnix(bss, bs, status=True):
    """Manchester decodes bitstream based on bitstrenght from GRC
    Based on the algorithm of nebarnix
    Source: <http://wiki.nebarnix.com/w/images/e/e0/POES.m>

    :param bss: array. float stream representing bit strength
    :param bs: bitarray. Input bit stream
    :param status: boolean. show progress bar
    :return bsd: bitarray. decoded bitstream
    """
    bsd = bitarray(len(bss//2))

    bitThreshold = 0.8
    idx2 = 10
    clockmod = 0
    errx = []

    with tqdm(total=len(bss), ncols=CLI_WIDTH, unit='bit', unit_scale=True, disable=not status) as pbar:
        for idx in range(1,bs.length()-3):
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
                        bsd[idx2] = 0
                    else:
                        bsd[idx2] = 1
                else:
                    if (bs[idx+1] == 1):
                        bsd[idx2] = 1
                    else:
                        bsd[idx2] = 0
                idx2 = idx2 + 1
            if idx % 1000 == 0: pbar.update(1000)

    return bsd


def gen_bitstream_v2(bss):
    """Generate bitstream from strenght array
    Version 2, which is much faster

    :param bss: array. float stream representing bit strength
    :return bs: bitarray. bitstream
    """
    bsn = bss >= 0
    bsp = np.packbits(bsn, axis=None)
    bs = bitarray()
    bs.frombytes(bsp.tobytes())
    
    return bs
    

# Only for debugging
#def compare_bs(bs1, bs2, perLine=64):
#    """Compare two bitarrays and mark differences
#
#    :param bs1: bitarray. bitsream 1
#    :param bs2: bitarray. bitstream 2
#    :param perLine: integer. number of bits per Line
#    """
#
#    length = min(bs1.length(), bs2.length())
#    for i in range(0, length, perLine):
#        result = '      '
#        for b in range(0,perLine):
#            if i+b < length:
#                if (bs1[i+b] == bs2[i+b]):
#                    result += ' '
#                else:
#                    result += '*'
#        if '*' in result:
#            print("%04d: %s" % (i/perLine, bs1[i:i + perLine].to01()))
#            print(result)


def print_format(bs, perLine=64):
    """Print bitarray with <perLine> Values per line with line counter

    :param bs: bitarray. bitsream
    :param perLine: integer. number of bits per Line
    """

    for i in range(0, bs.length(), perLine):
        print("%04d: %s" % (i//perLine,bs[i:i+perLine].to01()))

def party_check(minorFrame):
    """Perform parity check on minor frame

    :param minorFrame: bitarray.
    :return valid: bool.
    """

    # Word 103
    # Bit 1: CPU B data transfer incomplete bit
    # Bit 2: CPU A data transfer incomplete bit
    # Bit 3: Even parity check in words 2 through 18
    # Bit 4: Even parity check in words 19 thru 35
    # Bit 5: Even parity check in words 36 thru 52
    # Bit 6: Even parity check in words 53 thru 69
    # Bit 7: Even parity check in words 70 thru 86
    # Bit 8: Even parity check in words 87 thru bit 7 of word 103

    if minorFrame[2 * 8:19 * 8].count(1) % 2 != minorFrame[103*8 + 2]:
        return False
    if minorFrame[19 * 8:36 * 8].count(1) % 2 != minorFrame[103*8 + 3]:
        return False
    if minorFrame[36 * 8:53 * 8].count(1) % 2 != minorFrame[103*8 + 4]:
        return False
    if minorFrame[53 * 8:70 * 8].count(1) % 2 != minorFrame[103*8 + 5]:
        return False
    if minorFrame[70 * 8:87 * 8].count(1) % 2 != minorFrame[103*8 + 6]:
        return False
    if minorFrame[87 * 8:103 * 8 + 7].count(1) % 2 != minorFrame[103*8 + 7]:
        return False

    return True


def main():
    bitStreamStrength = []

    # Set values
    filename = ''  # input file
    outputFilename = 'NOAA_DSB_MinorFrames.txt'
    num = -1
    verbose = 0;
    bsFormat = 0;

    SyncWordInverse = bitarray(SyncWord)
    SyncWordInverse.invert()

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

    if verbose > 0:
        print('[INFO] Size: %d' % len(bitStreamStrength))
        print('[INFO] Duration: %0.2fs' % RawTime[-1])

    # Generate bitstream based on strength
    if verbose > 0: print("[INFO] Generate bitstream")
    bitStream = gen_bitstream_v2(bitStreamStrength)

    # Manchester decode bitstream
    if verbose > 0: print("[INFO] Decode bitstream")
    bitStreamDecoded = manchester_decode_nebarnix(bitStreamStrength, bitStream, verbose)

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
    idxSyncWord = bitStreamDecoded.search(SyncWord)
    idxSyncWordInv = bitStreamDecoded.search(SyncWordInverse)

    if verbose > 0:
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
        frame = bitarray(bitStreamDecoded[idx:idx+104*8])

        # Skip uncomplete frame
        if frame.length() != 832: continue

        if idx in idxSyncWord:
            minorFrames.append(frame)
        if idx in idxSyncWordInv:
            frame.invert()
            minorFrames.append(frame)

    # Detect Spacecraft ID
    spacecrafts = []
    for mf in minorFrames:
        spacecrafts.append(int(mf[16:24].to01(),2))

    if verbose > 2:
        for idx in range(0,len(minorFrames)):
            print()
            print("[INFO] Frame ", idx+1)
            print_format(minorFrames[idx], CLI_WIDTH)
            print("Spacecaft ID: ", spacecrafts[idx])
        print()

    # Most sendt spacecraft id
    spacecraft = stats.mode(spacecrafts)[0][0]

    if spacecraft == 8:
        print("[INFO] Detected Satellite: %d => NOAA-15" % spacecraft)
    elif spacecraft == 13:
        print("[INFO] Detected Satellite: %d => NOAA-18" % spacecraft)
    elif spacecraft == 15:
        print("[INFO] Detected Satellite: %d => NOAA-19" % spacecraft)
    else:
        print("[INFO] Detected Satellite: %d => UFO!!" % spacecraft)

    # Parity checks
    tmpMinorFrames= []
    for idx in range(0, len(minorFrames)):
        if not party_check(minorFrames[idx]):
            if verbose > 1:
                print()
                print("[WARN] Error in frame %d" % idx)
                print_format(minorFrames[idx], CLI_WIDTH)
        else:
            tmpMinorFrames.append(minorFrames[idx])
    minorFrames = tmpMinorFrames.copy()

    print("[INFO] Error free frames: ", len(minorFrames))

    # Save output to file
    try:
        outputFiledescriptor = open(outputFilename, "w")
    except:
        print("Error accessing file:", outputFilename)
        usage()

    if verbose > 0:
        print("[INFO] Saving data to ", outputFilename)

    with tqdm(total=len(minorFrames), ncols=CLI_WIDTH, unit='bit', unit_scale=True, disable=not verbose) as pbar:
        for idx in range(0, len(minorFrames)):
            mfHex = ''.join("%02X " % x for x in minorFrames[idx].tobytes())
            outputFiledescriptor.write(mfHex + '\n')
            pbar.update(1)

    outputFiledescriptor.close()

    print("Done.")


if __name__ == "__main__":
    main()