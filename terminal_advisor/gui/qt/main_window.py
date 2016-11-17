# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(437, 300)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.line_edit_advisee = QtWidgets.QLineEdit(self.centralWidget)
        self.line_edit_advisee.setObjectName("line_edit_advisee")
        self.gridLayout.addWidget(self.line_edit_advisee, 1, 0, 1, 1)
        self.list_advisees = QtWidgets.QListWidget(self.centralWidget)
        self.list_advisees.setObjectName("list_advisees")
        self.gridLayout.addWidget(self.list_advisees, 0, 0, 1, 1)
        self.combo_action = QtWidgets.QComboBox(self.centralWidget)
        self.combo_action.setObjectName("combo_action")
        self.combo_action.addItem("")
        self.combo_action.addItem("")
        self.gridLayout.addWidget(self.combo_action, 0, 3, 1, 1)
        self.button_run = QtWidgets.QPushButton(self.centralWidget)
        self.button_run.setObjectName("button_run")
        self.gridLayout.addWidget(self.button_run, 1, 3, 1, 1)
        self.button_refresh = QtWidgets.QPushButton(self.centralWidget)
        self.button_refresh.setObjectName("button_refresh")
        self.gridLayout.addWidget(self.button_refresh, 6, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.button_settings = QtWidgets.QPushButton(self.centralWidget)
        self.button_settings.setObjectName("button_settings")
        self.gridLayout.addWidget(self.button_settings, 6, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.status_bar = QtWidgets.QStatusBar(MainWindow)
        self.status_bar.setObjectName("status_bar")
        MainWindow.setStatusBar(self.status_bar)
        self.menu_bar = QtWidgets.QMenuBar(MainWindow)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 437, 22))
        self.menu_bar.setObjectName("menu_bar")
        self.menuFile = QtWidgets.QMenu(self.menu_bar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menu_bar)
        self.action_settings = QtWidgets.QAction(MainWindow)
        self.action_settings.setObjectName("action_settings")
        self.action_edit = QtWidgets.QAction(MainWindow)
        self.action_edit.setObjectName("action_edit")
        self.menuFile.addAction(self.action_settings)
        self.menuFile.addAction(self.action_edit)
        self.menu_bar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "terminal_advisor"))
        self.combo_action.setItemText(0, _translate("MainWindow", "Program Evaluation"))
        self.combo_action.setItemText(1, _translate("MainWindow", "Remove Advisor Hold"))
        self.button_run.setText(_translate("MainWindow", "Run"))
        self.button_refresh.setText(_translate("MainWindow", "Refresh"))
        self.button_settings.setText(_translate("MainWindow", "Settings"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.action_settings.setText(_translate("MainWindow", "Settings"))
        self.action_edit.setText(_translate("MainWindow", "Exit"))

