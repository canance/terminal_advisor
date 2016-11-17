#!/usr/bin/env python3

# source: https://nikolak.com/pyqt-qt-designer-getting-started/


from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtWidgets
from terminal_advisor.gui.qt import settings_window
from terminal_advisor.gui.threads import Save, Login
from terminal_advisor import __main__
import keyring


class GUIApp(QtWidgets.QMainWindow, settings_window.Ui_SettingsWindow):

    def __init__(self, advisor, config):
        super(self.__class__, self).__init__()
        self.advisor = advisor
        self.setupUi(self)
        self.config = config
        self.config = __main__.parse_config(__main__.get_args())
        self.login_thread = None
        self.save_thread = None

        # populate form fields
        self.line_edit_user.setText(config['DEFAULT']['user'])
        self.line_edit_url.setText(config['DEFAULT']['WebadvisorURL'])
        if config['KEYRING']['use'].lower().strip() == 'true':
            password = keyring.get_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'])
            self.line_edit_pass.setText(password)

        # connections
        self.button_login.clicked.connect(self.login)
        self.button_save.clicked.connect(self.save)

    @pyqtSlot()
    def login(self):
        # grab login data from form pass to thread
        base_url = self.line_edit_url.text()
        user = self.line_edit_user.text()
        password = self.line_edit_pass.text()

        self.login_thread = Login(self.advisor, base_url, user, password)
        self.login_thread.done.connect(self.login_done)
        self.login_thread.start()

    @pyqtSlot()
    def login_done(self):
        pass

    @pyqtSlot()
    def save(self):
        base_url = self.line_edit_url.text()
        user = self.line_edit_user.text()
        password = self.line_edit_pass.text()
        save_password = self.check_box_save_password.isChecked()

        self.save_thread = Save(self.advisor, base_url, user, password, save_password)
        self.save_thread.done.connect(self.save_done)
        self.save_thread.start()

    @pyqtSlot()
    def save_done(self):
        self.config = __main__.parse_config(__main__.get_args())
