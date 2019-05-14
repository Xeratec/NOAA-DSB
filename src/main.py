####################################################################################################
#                                              main.py                                             #
####################################################################################################
#                                                                                                  #
# Authors: Philip Wiese, Sevrin Mathys, Julian Merkofer                                            #
#                                                                                                  #
# Created: 16/04/19                                                                                #
#                                                                                                  #
# Purpose: Decoding the NOAA satellite telemetry beacons.                                          #
#          (reference: https://www1.ncdc.noaa.gov/pub/data/satellite/publications/podguides        #
#           /N-15%20thru%20N-19/pdf/2.1%20Section%204.0%20Real%20Time%20Data%20Systems%20for       #
#           %20Local%20Users%20.pdf)                                                               #
#                                                                                                  #
####################################################################################################


#*********************************#
#   load bit stream or waveform   #
#*********************************#
# rawStream = open("../TestFiles/NotMinePackedOut.txt").read()
bitStream = ''

# !!! use below when reading hex file
rawStream = open("../TestFiles/TestMinorFrame.txt").read()
rawStream = rawStream[:-1].replace(" ", "")

for elem in rawStream:
    bitStream += bin(int(elem, 16))[2:].zfill(4)


# !!! use below when reading bit file
# change from '\x01' to '1'
# for string in rawStream:
#     bitStream += str(ord(string))

wordStream = [[] for i in range(len(bitStream) / 832 + 1)]     # allocate space for minor frames


#*********************************************************#
#   look for sync word while looping through bit stream   #
#*********************************************************#
syncWord = '111011011110001000001000'      # where last 4 bits are spacecra
                                           # using '1000' at the moment
i = 0
while not bitStream == '':

    #   frame sync & SC ID [word pos: 0, 1, 2]   #
    #********************************************#
    idx = bitStream.find(syncWord)

    # end of bit stream
    if idx == -1:
        break

    # get index of next elem after sync word
    nextIdx = idx + len(syncWord)


    #   status [word pos: 3]   #
    #**************************#

    # CMD verification (cv) status
    if bitStream[nextIdx] == '0':
        wordStream[i].append('no cv update')
    else:
        wordStream[i].append('cv update')

    nextIdx += 1

    # TIP status
    if bitStream[nextIdx] == '0' and bitStream[nextIdx + 1] == '0':
        wordStream[i].append('orbital mode')
    elif bitStream[nextIdx] == '1' and bitStream[nextIdx + 1] == '0':
        wordStream[i].append('CPU memory dump mode')
    elif bitStream[nextIdx] == '0' and bitStream[nextIdx + 1] == '1':
        wordStream[i].append('dwell mode')
    else:
        wordStream[i].append('boost mode')

    nextIdx += 2

    # major frame count
    wordStream[i].append('major frame ' + str(int(bitStream[nextIdx : nextIdx + 3], 2)))
    nextIdx += 3


    #   dwell mode address [word pos: 3, 4]   #
    #*****************************************#
    wordStream[i].append('analog channel ' + str(int(bitStream[nextIdx: nextIdx + 9], 2)))
    nextIdx += 9


    #   minor frame counter [word pos: 4, 5]   #
    #******************************************#
    wordStream[i].append('minor frame ' + str(int(bitStream[nextIdx: nextIdx + 9], 2)))
    nextIdx += 9


    #   command verification [word pos: 6, 7]   #
    #*******************************************#
    # TODO: find out how this works
    nextIdx += 16


    #   time code [word pos: 8, 9, 10, 11, 12]   #
    #********************************************#
    # TODO: find out how this works & if and when it is needed
    # if needed:
    #     nextIdx += 40


    #   digital "B" subcom-1 [word pos: 8]   #
    #****************************************#
    wordStream[i].append('digital "B" 1 ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: find and understand encoding
    nextIdx += 8


    #   analog subcom (32 sec) [word pos: 9]   #
    #******************************************#
    wordStream[i].append('analog (32 sec) ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: decode to mV if needed
    nextIdx += 8


    #   analog subcom (16 sec) [word pos: 10]   #
    #*******************************************#
    wordStream[i].append('analog (16 sec) ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: decode to mV if needed
    nextIdx += 8


    #   analog subcom (1 sec) [word pos: 11]   #
    #******************************************#
    wordStream[i].append('analog (1 sec) ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: decode to mV if needed
    nextIdx += 8


    #   digital "B" subcom-2 [word pos: 12]   #
    #*****************************************#
    wordStream[i].append('digital "B" 2 ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: find and understand encoding
    nextIdx += 8


    #   analog subcom 2 (16 sec) [word pos: 13]   #
    #*********************************************#
    wordStream[i].append('analog 2 (16 sec) ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: find and understand encoding
    nextIdx += 8


    #   DAU 1 [word pos: 14]   #
    #**************************#
    wordStream[i].append('DAU 1 ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: find and understand encoding
    nextIdx += 8


    #   DAU 2 [word pos: 15]   #
    #**************************#
    wordStream[i].append('DAU 2 ' + bitStream[nextIdx: nextIdx + 8])
    # TODO: find and understand encoding
    nextIdx += 8


    #   HIRS/4 [word pos: 16, 17]   #
    #*******************************#
    wordStream[i].append('HIRS/4 ' + bitStream[nextIdx: nextIdx + 8] + ' ' +
                         bitStream[nextIdx + 8: nextIdx + 16])
    # TODO: find and understand encoding
    nextIdx += 16


    #   DCS-2 [word pos: 18, 19]   #
    #******************************#
    wordStream[i].append('DCS-2 ' + bitStream[nextIdx: nextIdx + 8] + ' ' +
                         bitStream[nextIdx + 8: nextIdx + 16])
    # TODO: find and understand encoding
    nextIdx += 16


    #   SEM [word pos: 20, 21]   #
    #****************************#
    wordStream[i].append('SEM ' + bitStream[nextIdx: nextIdx + 8] + ' ' +
                         bitStream[nextIdx + 8: nextIdx + 16])
    # TODO: find and understand encoding
    nextIdx += 16


    #   HIRS/4 [word pos: 22, 23, 26, 27, 30, 31, 34, 35, 38, 39, 42, 43, 54, 55, 58, 59, 62, 63,   #
    #                     66, 67, 70, 71, 74, 75, 78, 79, 82, 83, 84, 85, 88, 89, 92, 93]           #
    #***********************************************************************************************#
    tempIdx = nextIdx
    for j in range(19):

        # here are pos 36, 37 or 48, 49 that belong to SUBV/2 or CPU A
        if j == 6 or j == 7:
            tempIdx += 16
            continue

        wordStream[i][-3] += ' ' + bitStream[tempIdx + j * 16: tempIdx + 8 + j * 16] + ' ' + \
                             bitStream[tempIdx + 8 + j * 16: tempIdx + 16 + j * 16]
        # TODO: find and understand encoding
        # at pos 82, 83 -> 84, 85 no jump
        if not j == 17:
            tempIdx += 16

    nextIdx += 16


    #   DCS-2 [word pos: 24, 25, 28, 29, 32, 33, 40, 41, 44, 45, 52, 53, 56, 57, 60, 61   #
    #                    64, 65, 68, 69, 72, 73, 76, 77, 86, 87, 90, 91, 94, 95]          #
    #*************************************************************************************#
    tempIdx = nextIdx
    for j in range(18):

        # here are pos 36, 37 or 48, 49 or 80, 81 that belong to SUBV/2 or CPU A
        if j == 3 or j == 6 or j==14:
            tempIdx += 16
            continue

        # at pos 80, 81 -> 82, 83 extra jump
        elif j == 15:
            tempIdx += 16

        wordStream[i][-2] += ' ' + bitStream[tempIdx + j * 16: tempIdx + 8 + j * 16] + ' ' + \
                             bitStream[tempIdx + 8 + j * 16: tempIdx + 16 + j * 16]
        # TODO: find and understand encoding
        tempIdx += 16

    nextIdx += 6 * 16


    #   SBUV/2 [word pos: 36, 37]   #
    #*******************************#
    wordStream[i].append('SBUV/2 ' + bitStream[nextIdx: nextIdx + 8] + ' ' +
                         bitStream[nextIdx + 8: nextIdx + 16])
    # TODO: find and understand encoding
    nextIdx += 5 * 16


    #   CPU A [word pos: 46, 47, 48, 49, 50 ,51]   #
    #**********************************************#
    wordStream[i].append('CPU A ' + bitStream[nextIdx: nextIdx + 16] + ' ' +
                         bitStream[nextIdx + 16: nextIdx + 32] + ' '  +
                         bitStream[nextIdx + 32: nextIdx + 48])
    # TODO: find and understand encoding
    nextIdx += 17 * 16


    #   SBUV/2 [word pos: 80, 81]   #
    #*******************************#
    wordStream[i][-2] += ' ' + bitStream[nextIdx: nextIdx + 8] + ' ' + \
                         bitStream[nextIdx + 8: nextIdx + 16]
    # TODO: find and understand encoding
    nextIdx += 8 * 16


    #   CPU B [word pos: 96, 97, 98, 99, 100 ,101]   #
    #************************************************#
    wordStream[i].append('CPU B ' + bitStream[nextIdx: nextIdx + 16] + ' ' +
                         bitStream[nextIdx + 16: nextIdx + 32] + ' ' +
                         bitStream[nextIdx + 32: nextIdx + 48])
    # TODO: find and understand encoding
    nextIdx += 3 * 16


    # word 102 missing!
    nextIdx += 8


    #   CPU data status [word pos: 103]   #
    #*************************************#
    if bitStream[nextIdx] == '0' and bitStream[nextIdx + 1] == '0':
        wordStream[i].append('all CPU data received')
    elif bitStream[nextIdx] == '1' and bitStream[nextIdx + 1] == '0':
        wordStream[i].append('all CPU B data received')
    elif bitStream[nextIdx] == '0' and bitStream[nextIdx + 1] == '1':
        wordStream[i].append('all CPU A data received')
    else:
        wordStream[i].append('CPU A and CPU B data incomplete')

    nextIdx += 2


    #   parity [word pos: 103]   #
    #****************************#
    # TODO: do parity check
    nextIdx += 6


    # cut off read bits
    bitStream = bitStream[nextIdx:]

    # next (minor) frame
    i += 1


print(wordStream[-1])