####################################################################################################
#                                              main.py                                             #
####################################################################################################
#                                                                                                  #
# Authors: Philip Wiese, Sevrin Mathys, Julian Merkofer                                            #
#                                                                                                  #
# Created: 16/04/19                                                                                #
#                                                                                                  #
# Purpose: Decoding the NOAA satellite telemetry beacons.                                          #
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

wordStream = [[] for i in range(100)]     # allocate space for 100 minor frames


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
    if idx == -1: # or len(bitStream[idx:]) < 832:      # 832 (= 8 * 104) minor frame length
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
    # TODO: continue



    # cut off read bits
    bitStream = bitStream[nextIdx:]

    # next (minor) frame
    i += 1


print([minFrame for minFrame in wordStream if len(minFrame) > 0])