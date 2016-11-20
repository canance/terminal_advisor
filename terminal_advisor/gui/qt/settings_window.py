# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SettingsWindow(object):
    def setupUi(self, SettingsWindow):
        SettingsWindow.setObjectName("SettingsWindow")
        SettingsWindow.resize(414, 230)
        self.centralwidget = QtWidgets.QWidget(SettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label_url = QtWidgets.QLabel(self.centralwidget)
        self.label_url.setObjectName("label_url")
        self.gridLayout.addWidget(self.label_url, 0, 0, 1, 1)
        self.line_edit_url = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_url.setObjectName("line_edit_url")
        self.gridLayout.addWidget(self.line_edit_url, 0, 1, 1, 1)
        self.label_user = QtWidgets.QLabel(self.centralwidget)
        self.label_user.setObjectName("label_user")
        self.gridLayout.addWidget(self.label_user, 1, 0, 1, 1)
        self.line_edit_user = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_user.setObjectName("line_edit_user")
        self.gridLayout.addWidget(self.line_edit_user, 1, 1, 1, 1)
        self.button_login = QtWidgets.QPushButton(self.centralwidget)
        self.button_login.setObjectName("button_login")
        self.gridLayout.addWidget(self.button_login, 1, 2, 1, 1)
        self.label_pass = QtWidgets.QLabel(self.centralwidget)
        self.label_pass.setObjectName("label_pass")
        self.gridLayout.addWidget(self.label_pass, 2, 0, 1, 1)
        self.line_edit_pass = QtWidgets.QLineEdit(self.centralwidget)
        self.line_edit_pass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.line_edit_pass.setObjectName("line_edit_pass")
        self.gridLayout.addWidget(self.line_edit_pass, 2, 1, 1, 1)
        self.button_save = QtWidgets.QPushButton(self.centralwidget)
        self.button_save.setObjectName("button_save")
        self.gridLayout.addWidget(self.button_save, 3, 1, 1, 1)
        self.check_box_save_password = QtWidgets.QCheckBox(self.centralwidget)
        self.check_box_save_password.setObjectName("check_box_save_password")
        self.gridLayout.addWidget(self.check_box_save_password, 2, 2, 1, 1)
        SettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(SettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(SettingsWindow)

    def retranslateUi(self, SettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        SettingsWindow.setWindowTitle(_translate("SettingsWindow", "Settings"))
        self.label_url.setText(_translate("SettingsWindow", "Base URL"))
        self.label_user.setText(_translate("SettingsWindow", "User"))
        self.button_login.setText(_translate("SettingsWindow", "Login"))
        self.label_pass.setText(_translate("SettingsWindow", "Pass"))
        self.button_save.setText(_translate("SettingsWindow", "Save"))
        self.check_box_save_password.setText(_translate("SettingsWindow", "Save"))

