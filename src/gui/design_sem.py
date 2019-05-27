# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qtDesigner/SEM.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(559, 358)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.cbSource = QtWidgets.QComboBox(Form)
        self.cbSource.setObjectName("cbSource")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.gridLayout.addWidget(self.cbSource, 1, 1, 1, 1)

        self.retranslateUi(Form)
        self.cbSource.currentIndexChanged['int'].connect(Form.onSourceChange)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Data Source"))
        self.cbSource.setItemText(0, _translate("Form", "Proton Telescope"))
        self.cbSource.setItemText(1, _translate("Form", "Electron Telescope"))
        self.cbSource.setItemText(2, _translate("Form", "Proton Omnidirectional"))




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
