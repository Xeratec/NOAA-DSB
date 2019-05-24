from analyzer.minor_frame import MinorFrame
import datetime
from bitarray import bitarray
from dataclasses import dataclass



def main():
    bitStream = ''
    rawStream = open("../../NOAA_DSB_MinorFrames.txt").readlines()
    #rawStream = rawStream[167 -1]
    #rawStream = rawStream[441 -1]
    #rawStream = rawStream[762 -1]
    #rawStream = rawStream[1082-1]
    #rawStream = rawStream[1413-1]
    #rawStream = rawStream[1643-1]
    #rawStream = rawStream[1644-1]
    #rawStream = rawStream[1879-1]
    #rawStream = rawStream[2154-1]
    #rawStream = rawStream[2476-1]
    rawStream = rawStream[2796-1]
    #rawStream = rawStream[3110-1]
    #rawStream = rawStream[3410-1]
    rawStream = rawStream.replace(" ", "")
    rawStream = rawStream.replace("\n", "")

    print("### RAW Frame (HEX) ###")
    print("RAW   :    %s %s" % (len(rawStream), rawStream))

    for elem in rawStream:
        bitStream += bin(int(elem, 16))[2:].zfill(4)

    frame = MinorFrame(bitarray(bitStream))

    # Test if bitindex are correct
    # sliceFrame = frame.syncword + frame.status + frame.dwell_mode_address + frame.count + frame.command_verification \
    #         + frame.digital_b_subcom_1 + frame.analog_subcom_1_32 + frame.analog_subcom_1_16 + frame.analog_subcom_1_1 \
    #         + frame.digital_b_subcom_2 + frame.analog_subcom_2_16 + frame.dau_1 + frame.dau_2 + frame.hirs_4 \
    #         + frame.sem + frame.dcs_2 + frame.sbuv_2 + frame.cpu_a_telemetry + frame.cpu_b_telemetry + frame.miu_data \
    #         + frame.cpu_data_sataus + frame.parity
    #         # + frame.time_code
    #
    # sliceFrame[144:768] = frame.raw[144:768]
    #
    #
    # print_debug((sliceFrame ^ frame.raw).count(), "Diff  ")

    print()
    print("### RAW Frame Object ###")
    print_debug(frame.raw                   ,"RAW   ")
    print_debug(frame.syncword              ,"Sync  ")
    print_debug(frame.status                ,"Status")
    print_debug(frame.dwell_mode_address    ,"DWELL ")
    print_debug(frame.count                 ,"Count ")
    print_debug(frame.command_verification  ,"CMV   ")
    print_debug(frame.time_code             ,"Time  ")
    print_debug(frame.digital_b_subcom_1    ,"DBS1  ")
    print_debug(frame.analog_subcom_1_32    ,"AS1 32")
    print_debug(frame.analog_subcom_1_16    ,"AS1 16")
    print_debug(frame.analog_subcom_1_1     ,"AS1 1 ")
    print_debug(frame.digital_b_subcom_2    ,"DBS2  ")
    print_debug(frame.analog_subcom_2_16    ,"AS2 16")
    print_debug(frame.dau_1                 ,"DAU1  ")
    print_debug(frame.dau_2                 ,"DAZ2  ")
    print_debug(frame.hirs_4                ,"HIRS/4")
    print_debug(frame.sem                   ,"SEM   ")
    print_debug(frame.dcs_2                 ,"DCS2  ")
    print_debug(frame.sbuv_2                ,"SBUV  ")
    print_debug(frame.cpu_a_telemetry       ,"CPUA T")
    print_debug(frame.cpu_b_telemetry       ,"CPUB T")
    print_debug(frame.miu_data              ,"MIU   ")
    print_debug(frame.cpu_data_status       ,"CPU D ")
    print_debug(frame.parity                ,"Parity")

    print()
    print("### RAW Frame Object Functions ###")
    print_debug(frame.get_spacraft(),           "ID    ")
    print_debug(frame.parity_check(),           "Parity")
    print_debug(frame.get_status(),             "Status")
    print_debug(frame.get_count(),              "Count ")
    print_debug(frame.get_timestamp(),          "Time  ")
    print_debug(frame.get_dwell_address(),      "Dwell ")


def print_debug(msg, desc = ""):
    if isinstance(msg, MinorFrame.Data):
        if isinstance(msg.data, datetime.datetime):
            print("%s: %s" % (desc, msg.data))
        elif isinstance(msg.data, MinorFrame.Status):
            print("Status-CVS : %s" % msg.data.cmd_verification_status)
            print("Status-TIPS: %s" % msg.data.tip_status)
            print("Status-MFC : %s" % msg.data.major_frame_count)
        else:
            print("%s     : %s" % (desc, msg.data))

    elif isinstance(msg, bitarray):
        print("%s:  %3d %s" % (desc, int(msg.length()), msg))
    else:
        print("%s:      %s" % (desc, msg))




if __name__ == "__main__":
    main()

