#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
File name: noaa_dsb.py
Author: Philip Wiese
Date created: 17.05.2019
Date last modified: 17.05.2019
Python Version: 3

Example:
    $ python
"""

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QProcess, QTextCodec
from PyQt5.QtGui import QTextCursor

import sys
import os

from gui.design import design_main
from gui.design import design_stats
from gui.design import design_sem
from gui.design.settings import design_settings_analyze, design_settings_demod, design_settings_decode

DEBUG = True

class ExampleApp(QtWidgets.QMainWindow, design_main.Ui_MainWindow):

    #
    # Settings Variables
    #
    demod_baud_rate = 56250
    demod_log_level = 1
    decode_input_format = 0
    decode_log_level = 1
    analyze_log_level = 1


    def __init__(self):
        # Explaining super is out of the scope of this article
        # So please google it if you're not familar with it
        # Simple reason why we use it here is that it allows us to
        # access variables, methods etc in the design.py file
        super(self.__class__, self).__init__()
        self.setupUi(self)  # This is defined in design.py file automatically
                            # It sets up layout and widgets that are defined
        ui_stats = design_stats.Ui_Form()
        ui_stats.setupUi(self.wStats)

        ui_sem = design_sem.Ui_Form()
        ui_sem.setupUi(self.wSEM)

        # create a process output reader
        self.reader = ProcessOutputReader()
        self.reader.produce_output.connect(self.append_output)

        self.create_status_bar()

        if DEBUG:
            self.textDemodInput.setPlainText("/home/xeratec/Projects/NOAA-DSB/recordings/raw/NOAA-19_DSB_137-7700Mhz_2019-05-19_15-49-12.raw")
            self.textDemodOutput.setPlainText("/home/xeratec/Projects/NOAA-DSB/src/test/demod.raw")
            self.textDecodeInput.setPlainText("/home/xeratec/Projects/NOAA-DSB/src/test/demod.raw")
            self.textDecodeOutput.setPlainText("/home/xeratec/Projects/NOAA-DSB/src/test/NOAA.txt")

    #
    # Initialize statusbar
    #
    def create_status_bar(self):
        self.status_text = QtWidgets.QLabel("Ready")

        self.statusBar().addWidget(self.status_text, 1)

    #
    # Buttons
    #
    @pyqtSlot()
    def pbDemodOpen_clicked(self):
        file_choices = "RAW I/Q (*.raw);;All Files (*)"
        file = '' if self.textDemodInput.toPlainText() == '' else os.path.dirname(self.textDemodInput.toPlainText())
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select I/Q Recording', file, file_choices)
        if path:
            self.status_text.setText("Opened %s" % str(path))
            self.textDemodInput.setText(path)

    @pyqtSlot()
    def pbDemodSelect_clicked(self):
        file_choices = "RAW I/Q (*.raw)"
        file = os.path.join(os.path.curdir,
                            "Demod.raw") if self.textDemodOutput.toPlainText() == '' else self.textDemodOutput.toPlainText()
        path,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Demod File', file, file_choices)
        if path:
            self.status_text.setText("Selected %s" % str(path))
            self.textDemodOutput.setText(path)

    @pyqtSlot()
    def pbDecodeOpen_clicked(self):
        file_choices = "RAW I/Q (*.raw);;All Files (*)"
        file = '' if self.textDecodeInput.toPlainText() == '' else os.path.dirname(self.textDecodeInput.toPlainText())
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Demod File', file, file_choices)
        if path:
            self.status_text.setText("Opened %s" % str(path))
            self.textDecodeInput.setText(path)

    @pyqtSlot()
    def pbDecodeSelect_clicked(self):
        file_choices = "Frame File (*.txt)"
        file = os.path.join(os.path.curdir, "MinorFrames.txt") if self.textDecodeOutput.toPlainText() == '' else self.textDecodeOutput.toPlainText()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Frame File', file, file_choices)
        if path:
            self.status_text.setText("Selected %s" % str(path))
            self.textDecodeOutput.setText(path)

    @pyqtSlot()
    def pbAnalyzeOpen_clicked(self):
        file_choices = "Frames (*.txt);;All Files (*)"
        file = '' if self.textAnalyzeInput.toPlainText() == '' else os.path.dirname(self.textAnalyzeInput.toPlainText())
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Frame File', file, file_choices)
        if path:
            self.status_text.setText("Opend %s" % str(path))
            self.textAnalyzeInput.setText(path)

    @pyqtSlot()
    def pbAnalyzeSelect_clicked(self):
        file_choices = "Text File (*.txt)"
        file = os.path.join(os.path.curdir,
                            "Telemetry.txt") if self.textAnalyzeOutput.toPlainText() == '' else self.textAnalyzeOutput.toPlainText()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Text File',file, file_choices)
        if path:
            self.status_text.setText("Selected %s" % str(path))
            self.textAnalyzeOutput.setText(path)

    #
    # Settings Dialog
    #
    @pyqtSlot()
    def tbDemodSettings_clicked(self):
        DialogDemodSettings = QtWidgets.QDialog()
        ui = design_settings_demod.Ui_DialogDemodSettings()
        ui.setupUi(DialogDemodSettings)

        ui.cbBaudRate.setCurrentText(str(self.demod_baud_rate))
        ui.cbLogLevel.setCurrentIndex(self.demod_log_level)

        DialogDemodSettings.show()

        if DialogDemodSettings.exec_():
            self.demod_baud_rate = int(ui.cbBaudRate.currentText())
            self.demod_log_level = ui.cbLogLevel.currentIndex()


    @pyqtSlot()
    def tbDecodeSettings_clicked(self):
        DialogDecodeSettings = QtWidgets.QDialog()
        ui = design_settings_decode.Ui_DialogDecodeSettings()
        ui.setupUi(DialogDecodeSettings)

        ui.cbInputFormat.setCurrentIndex(self.decode_input_format)
        ui.cbLogLevel.setCurrentIndex(self.decode_log_level)

        DialogDecodeSettings.show()

        if DialogDecodeSettings.exec_():
            self.decode_input_format = ui.cbInputFormat.currentIndex()
            self.decode_log_level = ui.cbLogLevel.currentIndex()

    @pyqtSlot()
    def tbAnalyzeSettings_clicked(self):
        DialogAnalyzeSettings = QtWidgets.QDialog()
        ui = design_settings_analyze.Ui_DialogAnalyzeSettings()
        ui.setupUi(DialogAnalyzeSettings)

        ui.cbLogLevel.setCurrentIndex(self.analyze_log_level)

        DialogAnalyzeSettings.show()

        if DialogAnalyzeSettings.exec_():
            self.analyze_log_level = ui.cbLogLevel.currentIndex()

    #
    # Commands
    #
    @pyqtSlot()
    def run_demod(self):
        script = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'demodulator/noaa_demodulate.py')
        print(script)
        cmd = ['-u', script, '-r', str(self.demod_baud_rate), '-f', self.textDemodInput.toPlainText(), '-o', self.textDemodOutput.toPlainText()]
        print(cmd)
        self.reader.start('python2.7', cmd)

    @pyqtSlot()
    def run_decode(self):
        cmd = ['-u', 'decoder/noaa_decode.py', '-v', str(self.decode_log_level), '-i',str(self.decode_input_format),'-f', self.textDecodeInput.toPlainText(), '-o', self.textDecodeOutput.toPlainText()]
        print(cmd)
        self.reader.start('python3', cmd)

        return

    @pyqtSlot()
    def run_analyze(self):
        return

    #
    # Utility
    #
    @pyqtSlot(str)
    def append_output(self, text):
        self.tbProcess.textCursor().insertText(text)
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.tbProcess.textCursor()
        cursor.movePosition(QTextCursor.End)
      # cursor.movePosition(QTextCursor.Up if cursor.atBlockStart() else QTextCursor.StartOfLine)
        self.tbProcess.setTextCursor(cursor)


class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # merge stderr channel into stdout channel
        self.setProcessChannelMode(QProcess.MergedChannels)

        # prepare decoding process' output to Unicode
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()
        # only necessary when stderr channel isn't merged into stdout:
        # self._decoder_stderr = codec.makeDecoder()

        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        # only necessary when stderr channel isn't merged into stdout:
        # self.readyReadStandardError.connect(self._ready_read_standard_error)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)

    # only necessary when stderr channel isn't merged into stdout:
    # @pyqtSlot()
    # def _ready_read_standard_error(self):
    #     raw_bytes = self.readAllStandardError()
    #     text = self._decoder_stderr.toUnicode(raw_bytes)
    #     self.produce_output.emit(text)


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = ExampleApp()                 # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function    app.exec_()