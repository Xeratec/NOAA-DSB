#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
File name: noaa_demodulate.py
Author: Philip Wiese
Date created: 16.05.2019
Date last modified: 16.05.2019
Python Version: 2.7

Example:
    $ python noaa_decode.py -f ../../RandomGnuRadioStuff/6_bits_dcblock2.raw -v 1 -i 1
"""


from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
from gnuradio.filter import firdes
import pmt
import sys

def usage():
    """Prints help message."""
    print("Usage:")
    print("     -f <file>:         Input file (required)")
    print("     -s sample_rate:    Sample rate (default=56200)")
    print("     -i [0,1]:          Specify output format")
    print("                          0: Real Values (default)")
    print("                          1: Complex Values")
    print("     -o <file>:         Output file (default=demod_imag.raw)")
    sys.exit()

class noaa_demodulate(gr.top_block):
    def __init__(self, input_filename, _samp_rate, bs_format, output_filename):
        gr.top_block.__init__(self, "Noaa Demodulator")

        ##################################################
        # Variables
        ##################################################
        self.decimation = decimation = 1
        self.samp_rate = samp_rate = _samp_rate / decimation
        self.baud = baud = 8320
        self.sps = sps = samp_rate / (baud * 2.0)
        self.nfilts = nfilts = 72
        self.ebw = ebw = 0.25
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0 / float(sps), ebw, 64 * nfilts)
        self.lp_taps = lp_taps = firdes.low_pass_2(nfilts, nfilts, 2 / sps, 0.05, nfilts)
        self.bp_taps = bp_taps = firdes.band_pass_2(nfilts, nfilts, 0.1 / float(sps), 1.2 / float(sps), ebw, 64 * nfilts)

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
            interpolation=1,
            decimation=decimation,
            taps=None,
            fractional_bw=None,
        )
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(1, samp_rate, 11000, 6000, firdes.WIN_BLACKMAN, 6.76))
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, .068 / 1.5, (lp_taps), nfilts, 0, 10, 2)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(6, 1, .0000005, 2)
        self.dc_blocker_xx_0_0 = filter.dc_blocker_cc(16, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex * 1, samp_rate * 24, True)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_float * 1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_float * 1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float * 1)

        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(0.068 / 12, 6000 * 2 * 3.14159 / samp_rate,-6000 * 2 * 3.14159 / samp_rate)
        self.analog_agc2_xx_0 = analog.agc2_cc(0.5, 1, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)

        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex * 1, '/home/xeratec/Projects/NOAA-DSB/recordings/samples/POES_56k250.raw',
                                                       False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)

        if bs_format == 0:
            self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
            self.blocks_file_sink_3_1 = blocks.file_sink(gr.sizeof_float * 1, output_filename, False)
            self.blocks_file_sink_3_1.set_unbuffered(False)
        if bs_format == 1:
            self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, output_filename, False)
            self.blocks_file_sink_0.set_unbuffered(False)

        #################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.dc_blocker_xx_0_0, 0))

        if bs_format == 0:
            self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_file_sink_3_1, 0))
            self.connect((self.digital_cma_equalizer_cc_0, 0), (self.blocks_complex_to_imag_0, 0))
        if bs_format == 1:
            self.connect((self.digital_cma_equalizer_cc_0, 0), (self.blocks_file_sink_0, 0))

        self.connect((self.blocks_file_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.dc_blocker_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 3), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 1), (self.blocks_null_sink_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 2), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))

def main():
    filename = ''  # input file
    outputFilename = 'demod.raw'
    bsFormat = 0;
    sampleRate = 56250

    # Process Options
    ops = ['-f', '-i', '-o']

    while len(sys.argv) > 1:
        op = sys.argv.pop(1)
        if op == '-f':
            filename = sys.argv.pop(1)
        if op == '-i':
            bsFormat = int(sys.argv.pop(1))
        if op == '-o':
            outputFilename = sys.argv.pop(1)
        if op not in ops:
            print("Unknown option:")
            usage()

    if filename is '':
        usage()

    print "Demodulate to %s" % outputFilename
    try:
        noaa_demodulate(filename, sampleRate, bsFormat, outputFilename).run()
    except [[KeyboardInterrupt]]:
        pass

    print "Done."


if __name__ == '__main__':
    main()
