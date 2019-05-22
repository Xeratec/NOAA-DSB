# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtDesigner/settings/Settings_Analyze.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogAnalyzeSettings(object):
    def setupUi(self, DialogAnalyzeSettings):
        DialogAnalyzeSettings.setObjectName("DialogAnalyzeSettings")
        DialogAnalyzeSettings.resize(398, 121)
        self.gridLayout = QtWidgets.QGridLayout(DialogAnalyzeSettings)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(DialogAnalyzeSettings)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 0, 2, 1, 1)
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setObjectName("formLayout_3")
        self.lLogLevel = QtWidgets.QLabel(DialogAnalyzeSettings)
        self.lLogLevel.setObjectName("lLogLevel")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.lLogLevel)
        self.cbLogLevel = QtWidgets.QComboBox(DialogAnalyzeSettings)
        self.cbLogLevel.setObjectName("cbLogLevel")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.cbLogLevel.addItem("")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.cbLogLevel)
        self.gridLayout.addLayout(self.formLayout_3, 0, 1, 1, 1)

        self.retranslateUi(DialogAnalyzeSettings)
        self.cbLogLevel.setCurrentIndex(0)
        self.buttonBox.accepted.connect(DialogAnalyzeSettings.accept)
        self.buttonBox.rejected.connect(DialogAnalyzeSettings.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAnalyzeSettings)

    def retranslateUi(self, DialogAnalyzeSettings):
        _translate = QtCore.QCoreApplication.translate
        DialogAnalyzeSettings.setWindowTitle(_translate("DialogAnalyzeSettings", "Settings Analyzer"))
        self.lLogLevel.setText(_translate("DialogAnalyzeSettings", "Log Level"))
        self.cbLogLevel.setItemText(0, _translate("DialogAnalyzeSettings", "Quiet", "0"))
        self.cbLogLevel.setItemText(1, _translate("DialogAnalyzeSettings", "Normal", "1"))
        self.cbLogLevel.setItemText(2, _translate("DialogAnalyzeSettings", "Debug", "2"))
        self.cbLogLevel.setItemText(3, _translate("DialogAnalyzeSettings", "All", "3"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DialogAnalyzeSettings = QtWidgets.QDialog()
    ui = Ui_DialogAnalyzeSettings()
    ui.setupUi(DialogAnalyzeSettings)
    DialogAnalyzeSettings.show()
    sys.exit(app.exec_())
