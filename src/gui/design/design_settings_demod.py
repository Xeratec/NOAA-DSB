# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings/Settings_Demod.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogDemodSettings(object):
    def setupUi(self, DialogDemodSettings):
        DialogDemodSettings.setObjectName("DialogDemodSettings")
        DialogDemodSettings.resize(398, 121)
        self.gridLayout = QtWidgets.QGridLayout(DialogDemodSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogDemodSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 1, 1)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.lBaudRate = QtWidgets.QLabel(DialogDemodSettings)
        self.lBaudRate.setObjectName("lBaudRate")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lBaudRate)
        self.cbBaudRate = QtWidgets.QComboBox(DialogDemodSettings)
        self.cbBaudRate.setEditable(True)
        self.cbBaudRate.setInsertPolicy(QtWidgets.QComboBox.InsertAlphabetically)
        self.cbBaudRate.setObjectName("cbBaudRate")
        self.cbBaudRate.addItem("")
        self.cbBaudRate.addItem("")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbBaudRate)
        self.lLogLevel = QtWidgets.QLabel(DialogDemodSettings)
        self.lLogLevel.setObjectName("lLogLevel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lLogLevel)
        self.cbLogLevel = QtWidgets.QComboBox(DialogDemodSettings)
        self.cbLogLevel.setObjectName("cbLogLevel")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbLogLevel)
        self.gridLayout.addLayout(self.formLayout_3, 0, 1, 1, 1)

        self.retranslateUi(DialogDemodSettings)
        self.cbBaudRate.setCurrentIndex(1)
        self.cbLogLevel.setCurrentIndex(1)
        self.buttonBox.accepted.connect(DialogDemodSettings.accept)
        self.buttonBox.rejected.connect(DialogDemodSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogDemodSettings)

    def retranslateUi(self, DialogDemodSettings):
        _translate = QtCore.QCoreApplication.translate
        DialogDemodSettings.setWindowTitle(_translate("DialogDemodSettings", "Serrings Demodulator"))
        self.lBaudRate.setText(_translate("DialogDemodSettings", "Baud Rate"))
        self.cbBaudRate.setItemText(0, _translate("DialogDemodSettings", "48000"))
        self.cbBaudRate.setItemText(1, _translate("DialogDemodSettings", "562500"))
        self.lLogLevel.setText(_translate("DialogDemodSettings", "Log Level"))
        self.cbLogLevel.setItemText(0, _translate("DialogDemodSettings", "Quiet", "0"))
        self.cbLogLevel.setItemText(1, _translate("DialogDemodSettings", "Verbose", "1"))
        self.cbLogLevel.setItemText(2, _translate("DialogDemodSettings", "Debug", "2"))
        self.cbLogLevel.setItemText(3, _translate("DialogDemodSettings", "All", "3"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDemodSettings = QtWidgets.QDialog()
    ui = Ui_DialogDemodSettings()
    ui.setupUi(DialogDemodSettings)
    DialogDemodSettings.show()
    sys.exit(app.exec_())
