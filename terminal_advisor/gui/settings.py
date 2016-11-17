#!/usr/bin/env python3

# source: https://nikolak.com/pyqt-qt-designer-getting-started/

import sys

from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtWidgets
from terminal_advisor.gui.qt import settings_window
from terminal_advisor.gui.threads import Save, Login


class GUIApp(QtWidgets.QMainWindow, settings_window.Ui_SettingsWindow):

    def __init__(self, advisor):
        super(self.__class__, self).__init__()
        self.advisor = advisor
        self.setupUi(self)

        # connections
        self.button_login.clicked.connect(self.login)
        self.button_save.clicked.connect(self.save)

    @pyqtSlot()
    def login(self):
        # grab login data from form pass to thread
        base_url = self.line_edit_url.text()
        user = self.line_edit_user.text()
        password = self.line_edit_pass.text()

        login_thread = Login(base_url, user, password)
        login_thread.done.connect(self.login_done)
        login_thread.start()

    @pyqtSlot()
    def login_done(self):
        pass

    @pyqtSlot()
    def save(self):
        base_url = self.line_edit_url.text()
        user = self.line_edit_user.text()
        password = self.line_edit_pass.text()
        save_password = self.check_box_save_password.isChecked()
        save_thread = Save(base_url, user, password, save_password)
        save_thread.done.connect(self.save_done())
        save_thread.start()

    @pyqtSlot()
    def save_done(self):
        pass
