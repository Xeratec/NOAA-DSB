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


#*************#
#   imports   #
#*************#


#*********************************#
#   load bit stream or waveform   #
#*********************************#
rawStream = open("../TestFiles/NotMinePackedOut.txt").read()
bitStream = ''

# change from '\x01' to '1'
for string in rawStream:
    bitStream += str(ord(string))

wordStream = [[]]


#*********************************************************#
#   look for sync word while looping through bit stream   #
#*********************************************************#
syncWord = '11101101111000100000AAAA'      # where last 4 bits (AAAA) are spacecraft ID
                                           # TODO: find spacecraft ID
i = 0
while not bitStream == '':

    idx = bitStream.find(syncWord)

    # end of bit stream
    if idx < 0 or len(bitStream[idx:]) < 824:      # not sure if 824 (= 8 * 103) is correct yet
        break                                      # -> TODO: verify

    # get index of next elem after sync word
    nextIdx = bitStream.find(syncWord) + len(syncWord)


    #   status   #
    #************#

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


    #   dwell mode address   #
    #************************#



    # next frame
    i += 1


print(wordStream)