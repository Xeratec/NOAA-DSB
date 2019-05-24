#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: MajorFrame.py
Author: Philip Wiese
Date created: 23.05.2019
Date last modified: 23.05.2019
Python Version: 3

Object oriented minor frame implementation
TIP Minor Frame Format for NOAA-N,-N’

The TIP format is based on a major frame which contains 320 minor frames.
The Major Frame consists of 320 0.1 second Minor Frames

Additional Info:
The code documentations uses 'w' for 'word' and 'b' for 'bit'
Word number 3 is described as '3w'
"""

"""
TODO
* Write function documentation
* Finish implementation
"""


import datetime
from dataclasses import dataclass

class MinorFrame:
    # 1 Minor Frame is
    # 104 words total
    # 832 bits total

    # Raw minor frame data
    raw = None

    # Frame Sync and Spacecraft ID
    # 24 bit total
    # 0w: 11101101 (MSB) is first)
    # 1w: 11100010
    # 2w: 0000AAAA (Last 4 bits are spacecraft ID)
    syncword = None

    # Status
    # 6b total
    # 3w, 1b:   CMD verification (cv) status; 1=cv update word present in frame; 0=no cv update id frame
    # 3w, 2-3b: TIP status; 00=orbital mode;10=CPU Memory Dump Mode;01=Dwell Mode;11=Boost Mode
    # 3w, 4-6b: Major Frame Count; 000 Major Frame 0; 111=Major Frame 7; MSB first; Counter
    #           incremented every 320 minor frames
    status = None

    # Dwell Mode Address
    # 9 bit total
    # 3w, 7-8b:
    # 4w, 1-7b: 9 bit dwell mode address of analog channel that is being monitored continuously
    dwell_mode_address = None

    # Minor Frame Count
    # 9 bit total
    # 4w, 8b:
    # 5w, 1-8b: 000000000=Minor Frame 0, 100111111-Minor frame 319
    count = None

    # Command Verification
    # 16b total
    # 6w
    # 7w: Bits 9 thru 24 of each valid received or stored command word are placed in
    #     the 16 bit slots of telemetry words 6 and 7 on a one-for-one basis.
    command_verification = None

    # Time code (Minor Frame 0 only)
    # 40 bit total
    # 8w, 1-8b
    # 9w, 1b:   9 bits of binary Cay Count, MSB first
    # 9w, 2-5b: 0101, Spare Bits
    # 9w, 3-8b
    # 10w:
    # 11w:
    # 12w:      27 bits of Binary millisec of Day Count, MSB firs

    # Time code is inserted on word location 8-12 only in
    # minor frame 0 of every major frame. The data
    # inserted is referenced to the beginning of the first bit
    # of the minor frame sync word of minor frame 0
    # within ∀ millisecond.
    time_code = None

    # Digital "B" Subcom-1
    # 8 bit total
    # 8w:   A Subcommutation of Discrete Inputs collected to form 8 bit words. 256 Discrete
    #       Inputs (32 words) can be accommodated. It takes 32 frames to sample all inputs once
    #       (sampling rate=once/3.2 sec). A Major Frame contains 10 complete Digital “B”
    #       subcommutated frames.
    digital_b_subcom_1 = None

    # Analog Subcom-1 (32 sec)
    # 8 bit total
    # 9w:   A subcommutation of up to 191 analog points sampled once every 32 seconds plus
    #       64 analog points sampled twice every 32 seconds (once every 16 seconds).
    #       Bit 1 of each word represents 2560 mV, while Bit 8 represents 20 mV.
    analog_subcom_1_32 = None

    # Analog Subcom-1 (16 sec)
    # 8 bit total
    # 10w:  This subcommutation is controlled by a PROM located in the TIP and contains
    #       160 word locations with 128 analog channels sampled once every 16 seconds.
    analog_subcom_1_16 = None


    # Analog Subcom-1 (1 sec)
    # 8 bit total
    # 11w:  This subcommutation is controlled by a PROM in the TIP and contains 10
    #       analog channels sampled once every 1 second. Word 0 of this subcom is
    #       filled with data from an analog point selected by command. The selected
    #       analog point may be one of the 512 analog points available to the TIP.
    #       Bit on of each word represents 2560 mV while Bit 8 represents 20 mV.
    analog_subcom_1_1 = None

    # Digital "B" Subcom-2
    # 8 bit total
    # 12w:   The subcommutation of discrete inputs collected to form 8 Bit words.
    #       256 discrete inputs (32 words) can be accommodated. It takes 32 minor frames
    #       to sample all inputs once (sampling rate=once/3.2 sec). A Major Frame contains
    #       10 complete Digital “B” subcommutated frames.
    #       64 of these bit locations corresponding to TIP minor frames 24-31 form the
    #       XSU Digital “A” data. The XSU generates an 8 word subcom which is read out
    #       at the rate of one word per minor frame. The XSU subcom is synchronized with
    #       its word 1 in minor frame 24.
    digital_b_subcom_2 = None

    # Analog Subcom-2 (16)
    # 8 bit total
    # 13w:  This subcommutation is controlled by a PROM located in the TIP and contains 160
    #       words locations with 128 analog channels sampled once every 16 seconds.
    #       The remaining 32 word locations contain data from the Solar Array Telemetry
    #       Commutator Unit (SATCU). The SATCU receives inputs from 16 sources on the
    #       solar array, commutates them and presents this stream and presents it in the last 32
    #       word locations. The 32 words represent two successive passes through the SATCU subcom.
    analog_subcom_2_16 = None

    # DAU-1
    # 8 bit total
    # 14w:  8 Bit Housekeeping Telemetry words are formed by the DAU-1 and read out by the
    #       telemetry system at an average of 10 words per second.
    dau_1 = None

    # DAU-1
    # 8 bit total
    # 15w:  8 Bit Housekeeping Telemetry words are formed by the DAU-2 and read out by the
    #       telemetry system at an average of 10 words per second.
    dau_2 = None

    # HIRS/4
    # 288 bit total
    # 16-17w:
    # 22-23w:
    # 26-27w:
    # 30-31w:
    # 34-35w:
    # 38-39w:
    # 42-43w:
    # 54-55w:
    # 58-59w:
    # 62-63w:
    # 66-67w:
    # 70-71w:
    # 74-75w:
    # 78-79w:
    # 82-83w:
    # 84-85w:
    # 88-89w:
    # 92-93w:   8 Bit words are formed by the HIRS/3 experiment and are read out by the telemetry
    #           system at an average rate of 360 words per second.
    hirs_4 = None

    # SEM
    # 16 bit total
    # 20w:
    # 21w:  8 Bit words are formed by the SEM sensor and ready out by the telemetry system at
    #       an average rate of 20 words per second.
    sem = None

    # DCS-2
    # 256 bit total
    # 18-19w:
    # 24-25w:
    # 28-29w:
    # 32-33w:
    # 40-41w:
    # 44-45w:
    # 52-53w:
    # 56-57w:
    # 60-61w:
    # 64-65w:
    # 68-69w:
    # 72-73w:
    # 76-77w:
    # 86-87w:
    # 90-91w:
    # 94-95w:   8 Bit words are formed by the DCS experiment and are read out by the telemetry
    #           system at an average rate of 320 words per second
    dcs_2 = None

    # SBUF/2
    # 32 bit total
    # 36-37w:
    # 80-81w:   8 Bit words are formed by the SBUV/2 experiment and read out by the telemetry
    #           system at an average rate of 40 words per second.
    sbuv_2 = None

    # CPU A Telemetry
    # 48 bit total
    # 46-47w:
    # 48-49w:
    # 50-51w:  A second block of 16 Bit CPU words is ready out by the telemetry system every minor frame.
    cpu_a_telemetry = None

    # CPU B Telemetry
    # 48 bit total
    # 96-97w:
    # 98-99w:
    # 100-101w:  A second block of 16 Bit CPU words is ready out by the telemetry system every minor frame.
    cpu_b_telemetry = None

    # IMPORTANT! THIS MAY BE INCORRECT
    # MIU (MHS interface unit)
    # 8 bit total
    # 102w, 1-2b:   Reserved
    # 102w, 2-4b:   000: Telemetry Mode: Normal (NORM)
    #               001: Fast Dump (FADU)
    #               010: Slow Dump (SLDU)
    #               011: Very Slow Dump (VSDU)
    #               100: Bus Eng Mode (BEM)
    #               101: Undefined (UNDF)
    #               110: Undefined
    #               111: Undefined
    # 102w, 5b:     TIP ENGR Frame Enabled
    #               1: Enabled
    #               0: Disabled
    # 102w, 6-7b:   MIU ID
    #               00: MIU 1
    #               01: MIU 2
    #               11: Single MIU
    miu_data = None


    # CPU Data Status
    # 2 bit total
    # 103w, 1-2b:   00: All CPU data received
    #               01: All CPU A data received; CPU B data incomplete
    #               10: All CPU B data received; CPU A data incomplete
    #               11: CPU A and CPU B data incomplete
    cpu_data_status = None

    # Parity
    # 6 bit total
    # 103, 3-7b:    Bit 1: CPU B data transfer incomplete bit
    #               Bit 2: CPU A data transfer incomplete bit
    #               Bit 3: Even parity check in words 2 through 18
    #               Bit 4: Even parity check in words 19 thru 35
    #               Bit 5: Even parity check in words 36 thru 52
    #               Bit 6: Even parity check in words 53 thru 69
    #               Bit 7: Even parity check in words 70 thru 86
    #               Bit 8: Even parity check in words 87 thru bit 7 of word 103
    parity = [None, None, None, None, None, None]

    @dataclass
    class Status:
        """
        CMD verification (cv) status; 1=cv update word present in frame; 0=no cv update id frame
        TIP status; 00=orbital mode;10=CPU Memory Dump Mode;01=Dwell Mode;11=Boost Mode
        Major Frame Count; 000 Major Frame 0; 111=Major Frame 7; MSB first; Counter incremented every 320 minor frames
        """
        major_frame_count = None
        cmd_verification_status = None
        tip_status = None

    @dataclass
    class Data:
         """
         Returned object of get-methods
         Attributes:
            :key data: bitstring or class (Status). Data
            :key data: boolean. Parity bit valid for data
         """
         data = None
         parity = None

    def __init__(self, raw=None):
        if raw is None: raise ValueError

        self.raw = raw
        self.syncword = raw[0:24]
        self.status = raw[24:30]
        self.dwell_mode_address = raw[30:39]
        self.count = raw[39:48]
        self.command_verification = raw[48:64]
        self.time_code = raw[64:104]
        self.digital_b_subcom_1 = raw[64:72]
        self.analog_subcom_1_32 = raw[72:80]
        self.analog_subcom_1_16 = raw[80:88]
        self.analog_subcom_1_1 = raw[88:96]
        self.digital_b_subcom_2 = raw[96:104]
        self.analog_subcom_2_16 = raw[104:112]
        self.dau_1 = raw[112:120]
        self.dau_2 = raw[120:128]
        self.hirs_4 = raw[128:144] + raw[176:192] + raw[208:224] + raw[240:256] \
                    + raw[272:288] + raw[304:320] + raw[336:352] + raw[432:448] \
                    + raw[464:480] + raw[496:512] + raw[528:544] + raw[560:576] \
                    + raw[592:608] + raw[624:640] + raw[656:672] + raw[672:688] \
                    + raw[704:720] + raw[736:752]
        self.sem = raw[160:176]
        self.dcs_2 = raw[144:160] + raw[192:208] + raw[224:240] + raw[256:272] \
                   + raw[320:336] + raw[352:368] + raw[416:432] + raw[448:464] \
                   + raw[480:496] + raw[512:528] + raw[544:560] + raw[576:592] \
                   + raw[608:624] + raw[688:704] + raw[720:736] + raw[752:768]
        self.sbuv_2 = raw[288:304] + raw[640:656]
        self.cpu_a_telemetry = raw[368:416]
        self.cpu_b_telemetry = raw[768:816]
        self.miu_data = raw[816:824]
        self.cpu_data_status = raw[824:826]
        self.parity = raw[826:832]

    # TODO
    def get_spacraft(self):
        return NotImplemented

    def get_status(self):
        s = self.Status()
        s.major_frame_count = int(self.status[4:7].to01(), 2)
        s.cmd_verification_status = int(self.status[0:2].to01(), 2)
        s.tip_status = int(self.status[2:4].to01(), 2)

        r = self.Data()
        r.parity = True if self.parity_check().data[0] else False
        r.data = s

        return r

    def get_dwell_address(self):
        r = self.Data()
        r.parity =  True if self.parity_check().data[0]  else False
        r.data = int(self.dwell_mode_address.to01(), 2)

        return r

    def get_count(self):
        r = self.Data()
        r.parity = True if self.parity_check().data[0] else False
        r.data = int(self.count.to01(), 2)
        return r

    def get_command_verification(self):
        r = self.Data()
        r.parity = True if self.parity_check().data[0]  else False
        r.data = self.command_verification

        return r

    def get_timestamp(self):
        if self.get_count().data != 0: return None

        day_count = int(self.time_code[0:9].to01(),2)
        hour_minute_second = int(self.time_code[13:40].to01(),2)
        hms = datetime.timedelta(days=day_count, milliseconds=hour_minute_second)

        r = self.Data()
        r.parity = True if self.parity_check().data[0]  else False
        r.data = hms

        return r

    # TODO
    # Data on multi frames
    def get_subcom_1(self):
        return NotImplemented

    # Data on multi frames
    # No documentation?
    def get_subcom_2(self):
        return NotImplemented

    # No documentation?
    def get_dau(self):
        return NotImplemented

    # Data on multi frames
    def get_hirs_4(self):
        return self.hirs_4

    def get_sem(self):
        return self.sems

    def get_dcs_2(self):
        return NotImplemented

    # No documentation?
    def get_sbuv_2(self):
        return NotImplemented

    # No documentation?
    def get_cpu_telemetry(self):
        return NotImplemented

    def get_cpu_data_status(self):
        return self.cpu_data_status

    def parity_check(self):
        """Perform parity check on minor frame

        :return valid: bool.
        """
        r = self.Data()
        r.data = [True, True, True, True, True, True]
        r.parity = True
        if self.raw[16:152].count(1) % 2 != self.parity[0]:
            r.data[0] = False
        if self.raw[152:288].count(1) % 2 != self.parity[1]:
            r.data[1] = False
        if self.raw[288:424].count(1) % 2 != self.parity[2]:
            r.data[2] = False
        if self.raw[424:560].count(1) % 2 != self.parity[3]:
            r.data[3] = False
        if self.raw[560:696].count(1) % 2 != self.parity[4]:
            r.data[4] = False
        if self.raw[696:831].count(1) % 2 != self.parity[5]:
            r.data[5] = False
            r.parity = False

        return r


