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
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.buttonRefresh = QtWidgets.QPushButton(self.centralWidget)
        self.buttonRefresh.setObjectName("buttonRefresh")
        self.gridLayout.addWidget(self.buttonRefresh, 6, 0, 1, 1)
        self.buttonRun = QtWidgets.QPushButton(self.centralWidget)
        self.buttonRun.setObjectName("buttonRun")
        self.gridLayout.addWidget(self.buttonRun, 1, 3, 1, 1)
        self.comboAction = QtWidgets.QComboBox(self.centralWidget)
        self.comboAction.setObjectName("comboAction")
        self.comboAction.addItem("")
        self.comboAction.addItem("")
        self.gridLayout.addWidget(self.comboAction, 0, 3, 1, 1)
        self.listWidgetAdvisees = QtWidgets.QListWidget(self.centralWidget)
        self.listWidgetAdvisees.setObjectName("listWidgetAdvisees")
        self.gridLayout.addWidget(self.listWidgetAdvisees, 0, 0, 1, 1)
        self.txtAdviseeSearch = QtWidgets.QLineEdit(self.centralWidget)
        self.txtAdviseeSearch.setObjectName("txtAdviseeSearch")
        self.gridLayout.addWidget(self.txtAdviseeSearch, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionUsername = QtWidgets.QAction(MainWindow)
        self.actionUsername.setObjectName("actionUsername")
        self.actionBase_URL = QtWidgets.QAction(MainWindow)
        self.actionBase_URL.setObjectName("actionBase_URL")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "terminal_advisor"))
        self.buttonRefresh.setText(_translate("MainWindow", "Refresh"))
        self.buttonRun.setText(_translate("MainWindow", "Run"))
        self.comboAction.setItemText(0, _translate("MainWindow", "Program Evaluation"))
        self.comboAction.setItemText(1, _translate("MainWindow", "Remove Advisor Hold"))
        self.actionUsername.setText(_translate("MainWindow", "Username"))
        self.actionBase_URL.setText(_translate("MainWindow", "Base URL"))

