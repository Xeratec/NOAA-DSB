#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Tue Apr 30 11:45:22 2019
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import pmt
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.decimation = decimation = 1
        self.samp_rate = samp_rate = 50e3/decimation
        self.baud = baud = 8320
        self.sps = sps = samp_rate/(baud*2.0)
        self.nfilts = nfilts = 72
        self.ebw = ebw = 0.25
        self.rrc_taps = rrc_taps = firdes.root_raised_cosine(nfilts,nfilts, 1.0/float(sps),ebw,64*nfilts)
        self.lp_taps = lp_taps = firdes.low_pass_2(nfilts,nfilts, 2/sps,0.05,nfilts)
        self.bp_taps = bp_taps = firdes.band_pass_2(nfilts,nfilts, 0.1/float(sps), 1.2/float(sps),ebw,64*nfilts)

        self.NOAA_DSB_Constellation = NOAA_DSB_Constellation = digital.constellation_bpsk().base()


        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=decimation,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	1024, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	'QT GUI Plot', #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not True:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-80, -20)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win)
        self.qtgui_number_sink_0_1 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0_1.set_update_time(0.25)
        self.qtgui_number_sink_0_1.set_title('Bitrate')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0_1.set_min(i, -1)
            self.qtgui_number_sink_0_1.set_max(i, 1)
            self.qtgui_number_sink_0_1.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_1.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_1.set_label(i, labels[i])
            self.qtgui_number_sink_0_1.set_unit(i, units[i])
            self.qtgui_number_sink_0_1.set_factor(i, factor[i])

        self.qtgui_number_sink_0_1.enable_autoscale(True)
        self._qtgui_number_sink_0_1_win = sip.wrapinstance(self.qtgui_number_sink_0_1.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_1_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.25)
        self.qtgui_number_sink_0.set_title('Error')

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_const_sink_x_0_0_0_0 = qtgui.const_sink_c(
        	1024, #size
        	'QT GUI Plot', #name
        	1 #number of inputs
        )
        self.qtgui_const_sink_x_0_0_0_0.set_update_time(0.05)
        self.qtgui_const_sink_x_0_0_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0_0_0.enable_axis_labels(True)

        if not True:
          self.qtgui_const_sink_x_0_0_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
                  "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0_0_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_const_sink_x_0_0_0_0_win)
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, 11000, 6000, firdes.WIN_BLACKMAN, 6.76))
        self.digital_pfb_clock_sync_xxx_0 = digital.pfb_clock_sync_ccf(sps, .068/1.5, (lp_taps), nfilts, 0, 10, 2)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.digital_constellation_decoder_cb_0 = digital.constellation_decoder_cb(NOAA_DSB_Constellation)
        self.digital_cma_equalizer_cc_0 = digital.cma_equalizer_cc(6, 1, .0000005, 2)
        self.dc_blocker_xx_0_0 = filter.dc_blocker_cc(16, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate*24,True)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_gr_complex*1, 'C:\\Users\\Sevy\\Desktop\\School\\ETH\\SDR\\POES_56k250.raw', False)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)
        self.blocks_file_sink_1 = blocks.file_sink(gr.sizeof_char*1, 'C:\\Users\\Sevy\\Desktop\\School\\ETH\\SDR\\NotMinePackedOut.txt', False)
        self.blocks_file_sink_1.set_unbuffered(False)
        self.analog_pll_carriertracking_cc_0 = analog.pll_carriertracking_cc(0.068/12, 6000*2*3.14159/samp_rate, -6000*2*3.14159/samp_rate)
        self.analog_agc2_xx_0 = analog.agc2_cc(0.5, 1, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.analog_pll_carriertracking_cc_0, 0))
        self.connect((self.analog_pll_carriertracking_cc_0, 0), (self.dc_blocker_xx_0_0, 0))
        self.connect((self.blocks_file_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_file_sink_1, 0))
        self.connect((self.blocks_throttle_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.dc_blocker_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.digital_constellation_decoder_cb_0, 0))
        self.connect((self.digital_cma_equalizer_cc_0, 0), (self.qtgui_const_sink_x_0_0_0_0, 0))
        self.connect((self.digital_constellation_decoder_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 3), (self.blocks_null_sink_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 0), (self.digital_cma_equalizer_cc_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 1), (self.qtgui_number_sink_0, 0))
        self.connect((self.digital_pfb_clock_sync_xxx_0, 2), (self.qtgui_number_sink_0_1, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_pfb_clock_sync_xxx_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_samp_rate(50e3/self.decimation)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_sps(self.samp_rate/(self.baud*2.0))
        self.qtgui_waterfall_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, 11000, 6000, firdes.WIN_BLACKMAN, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate*24)
        self.analog_pll_carriertracking_cc_0.set_max_freq(6000*2*3.14159/self.samp_rate)
        self.analog_pll_carriertracking_cc_0.set_min_freq(-6000*2*3.14159/self.samp_rate)

    def get_baud(self):
        return self.baud

    def set_baud(self, baud):
        self.baud = baud
        self.set_sps(self.samp_rate/(self.baud*2.0))

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_lp_taps(firdes.low_pass_2(self.nfilts,self.nfilts, 2/self.sps,0.05,self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts, 1.0/float(self.sps),self.ebw,64*self.nfilts))
        self.set_bp_taps(firdes.band_pass_2(self.nfilts,self.nfilts, 0.1/float(self.sps), 1.2/float(self.sps),self.ebw,64*self.nfilts))

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts
        self.set_lp_taps(firdes.low_pass_2(self.nfilts,self.nfilts, 2/self.sps,0.05,self.nfilts))
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts, 1.0/float(self.sps),self.ebw,64*self.nfilts))
        self.set_bp_taps(firdes.band_pass_2(self.nfilts,self.nfilts, 0.1/float(self.sps), 1.2/float(self.sps),self.ebw,64*self.nfilts))

    def get_ebw(self):
        return self.ebw

    def set_ebw(self, ebw):
        self.ebw = ebw
        self.set_rrc_taps(firdes.root_raised_cosine(self.nfilts,self.nfilts, 1.0/float(self.sps),self.ebw,64*self.nfilts))
        self.set_bp_taps(firdes.band_pass_2(self.nfilts,self.nfilts, 0.1/float(self.sps), 1.2/float(self.sps),self.ebw,64*self.nfilts))

    def get_rrc_taps(self):
        return self.rrc_taps

    def set_rrc_taps(self, rrc_taps):
        self.rrc_taps = rrc_taps

    def get_lp_taps(self):
        return self.lp_taps

    def set_lp_taps(self, lp_taps):
        self.lp_taps = lp_taps
        self.digital_pfb_clock_sync_xxx_0.update_taps((self.lp_taps))

    def get_bp_taps(self):
        return self.bp_taps

    def set_bp_taps(self, bp_taps):
        self.bp_taps = bp_taps

    def get_NOAA_DSB_Constellation(self):
        return self.NOAA_DSB_Constellation

    def set_NOAA_DSB_Constellation(self, NOAA_DSB_Constellation):
        self.NOAA_DSB_Constellation = NOAA_DSB_Constellation


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
