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

from gui import design_main
from gui import design_stats
from gui import design_sem
from gui.settings import design_settings_analyze, design_settings_demod, design_settings_decode

##### DEBUG ONLY ######
DEBUG = True
#######################

class NOAA_DSB(QtWidgets.QMainWindow, design_main.Ui_MainWindow):

    #
    # Settings Variables
    #
    demod_baud_rate = 56250
    demod_log_level = 1
    decode_input_format = 0
    decode_log_level = 1
    analyze_log_level = 1


    def __init__(self):
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
        self.reader.produce_finished.connect(self.cmd_finished)

        self.create_status_bar()

        if DEBUG:
            self.textDemodInput.setPlainText("/home/xeratec/Projects/NOAA-DSB/recordings/samples/POES_56k250.raw")
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
            self.setStatusBarText("Opened ",str(path))
            self.textDemodInput.setText(path)

    @pyqtSlot()
    def pbDemodSelect_clicked(self):
        file_choices = "RAW I/Q (*.raw)"
        file = os.path.join(os.path.curdir,
                            "Demod.raw") if self.textDemodOutput.toPlainText() == '' else self.textDemodOutput.toPlainText()
        path,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Demod File', file, file_choices)
        if path:
            self.setStatusBarText("Selected ", str(path))
            self.textDemodOutput.setText(path)

    @pyqtSlot()
    def pbDecodeOpen_clicked(self):
        file_choices = "RAW I/Q (*.raw);;All Files (*)"
        file = '' if self.textDecodeInput.toPlainText() == '' else os.path.dirname(self.textDecodeInput.toPlainText())
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Demod File', file, file_choices)
        if path:
            self.setStatusBarText("Opened ", str(path))
            self.textDecodeInput.setText(path)

    @pyqtSlot()
    def pbDecodeSelect_clicked(self):
        file_choices = "Frame File (*.txt)"
        file = os.path.join(os.path.curdir, "MinorFrames.txt") if self.textDecodeOutput.toPlainText() == '' else self.textDecodeOutput.toPlainText()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Frame File', file, file_choices)
        if path:
            self.setStatusBarText("Selected ", str(path))
            self.textDecodeOutput.setText(path)

    @pyqtSlot()
    def pbAnalyzeOpen_clicked(self):
        file_choices = "Frames (*.txt);;All Files (*)"
        file = '' if self.textAnalyzeInput.toPlainText() == '' else os.path.dirname(self.textAnalyzeInput.toPlainText())
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select Frame File', file, file_choices)
        if path:
            self.setStatusBarText("Opend ", str(path))
            self.textAnalyzeInput.setText(path)

    @pyqtSlot()
    def pbAnalyzeSelect_clicked(self):
        file_choices = "Text File (*.txt)"
        file = os.path.join(os.path.curdir,
                            "Telemetry.txt") if self.textAnalyzeOutput.toPlainText() == '' else self.textAnalyzeOutput.toPlainText()
        path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save Text File',file, file_choices)
        if path:
            self.setStatusBarText("Selected ", str(path))
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
            print(self.demod_log_level)


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
        cmd = ['-u', script, '-v', str(self.demod_log_level),'-r', str(self.demod_baud_rate), '-f', self.textDemodInput.toPlainText(), '-o', self.textDemodOutput.toPlainText()]

        self.reader.start('python2.7', cmd)

    @pyqtSlot()
    def run_decode(self):
        script = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'decoder/noaa_decode.py')
        cmd = ['-u', script, '-v', str(self.decode_log_level), '-i',str(self.decode_input_format),'-f', self.textDecodeInput.toPlainText(), '-o', self.textDecodeOutput.toPlainText()]
        self.reader.start('python3', cmd)

    @pyqtSlot()
    def run_analyze(self):
        return


    #
    # Menu entry
    #
    def onAbout(self):
        file = open('gui/about.txt', 'r')
        text = file.read()

        file.close()
        msg = QtWidgets.QMessageBox()
        msg.setInformativeText(text.strip())
        msg.setWindowTitle("About NOAA DSB Decoder")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()



    def onLicense(self):
        file = open('gui/license.txt', 'r')
        text = file.read()

        file.close()
        msg = QtWidgets.QMessageBox()
        msg.setInformativeText(text.strip())
        msg.setWindowTitle("License")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
    #
    # Utility
    #
    def setStatusBarText(self, msg, text=None):
        if text==None:
            self.status_text.setText(msg)
            return

        if len(text) + len(msg) > 64:
            self.status_text.setText(msg +".. " + text[-(64-len(msg)):])
        else:
            self.status_text.setText(msg + text)

    def cmd_finished(self, exitCode):
        if exitCode == 0:
            self.setStatusBarText("Done")
        else:
            self.setStatusBarText("Error")

    @pyqtSlot(str)
    def append_output(self, text):
        self.tbProcess.textCursor().insertText(text)

        self.setStatusBarText(text.split('\n')[-1])
        self.scroll_to_last_line()

    def scroll_to_last_line(self):
        cursor = self.tbProcess.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.tbProcess.setTextCursor(cursor)


class ProcessOutputReader(QProcess):
    produce_output = pyqtSignal(str)
    produce_finished = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # merge stderr channel into stdout channel
        self.setProcessChannelMode(QProcess.MergedChannels)

        # prepare decoding process' output to Unicode
        codec = QTextCodec.codecForLocale()
        self._decoder_stdout = codec.makeDecoder()

        self.readyReadStandardOutput.connect(self._ready_read_standard_output)
        self.finished.connect(self.onFinished)

    @pyqtSlot()
    def _ready_read_standard_output(self):
        raw_bytes = self.readAllStandardOutput()
        text = self._decoder_stdout.toUnicode(raw_bytes)
        self.produce_output.emit(text)

    def onFinished(self, exitCode):
        self.produce_finished.emit(exitCode)


def main():
    app = QtWidgets.QApplication(sys.argv)  # A new instance of QApplication
    form = NOAA_DSB()                  # We set the form to be our ExampleApp (design)
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function    app.exec_()