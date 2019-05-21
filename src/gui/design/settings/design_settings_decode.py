# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Settings_Decode.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogDecodeSettings(object):
    def setupUi(self, DialogDecodeSettings):
        DialogDecodeSettings.setObjectName("DialogDecodeSettings")
        DialogDecodeSettings.resize(398, 121)
        self.gridLayout = QtWidgets.QGridLayout(DialogDecodeSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogDecodeSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 1, 1)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.lLogLevel = QtWidgets.QLabel(DialogDecodeSettings)
        self.lLogLevel.setObjectName("lLogLevel")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.lLogLevel)
        self.cbLogLevel = QtWidgets.QComboBox(DialogDecodeSettings)
        self.cbLogLevel.setObjectName("cbLogLevel")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cbLogLevel)
        self.lInputFormat = QtWidgets.QLabel(DialogDecodeSettings)
        self.lInputFormat.setObjectName("lInputFormat")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lInputFormat)
        self.cbInputFormat = QtWidgets.QComboBox(DialogDecodeSettings)
        self.cbInputFormat.setObjectName("cbInputFormat")
        self.cbInputFormat.addItem("")
        self.cbInputFormat.addItem("")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbInputFormat)
        self.gridLayout.addLayout(self.formLayout_3, 0, 1, 1, 1)

        self.retranslateUi(DialogDecodeSettings)
        self.cbLogLevel.setCurrentIndex(1)
        self.buttonBox.accepted.connect(DialogDecodeSettings.accept)
        self.buttonBox.rejected.connect(DialogDecodeSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogDecodeSettings)

    def retranslateUi(self, DialogDecodeSettings):
        _translate = QtCore.QCoreApplication.translate
        DialogDecodeSettings.setWindowTitle(_translate("DialogDecodeSettings", "Dialog"))
        self.lLogLevel.setText(_translate("DialogDecodeSettings", "Log Level"))
        self.cbLogLevel.setItemText(0, _translate("DialogDecodeSettings", "Quiet", "0"))
        self.cbLogLevel.setItemText(1, _translate("DialogDecodeSettings", "Verbose", "1"))
        self.cbLogLevel.setItemText(2, _translate("DialogDecodeSettings", "Debug", "2"))
        self.cbLogLevel.setItemText(3, _translate("DialogDecodeSettings", "All", "3"))
        self.lInputFormat.setText(_translate("DialogDecodeSettings", "Input Format"))
        self.cbInputFormat.setItemText(0, _translate("DialogDecodeSettings", "Float32"))
        self.cbInputFormat.setItemText(1, _translate("DialogDecodeSettings", "Complex64"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogDecodeSettings = QtWidgets.QDialog()
    ui = Ui_DialogDecodeSettings()
    ui.setupUi(DialogDecodeSettings)
    DialogDecodeSettings.show()
    sys.exit(app.exec_())
