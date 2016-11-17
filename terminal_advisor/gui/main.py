#!/usr/bin/env python3

# source: https://nikolak.com/pyqt-qt-designer-getting-started/

import sys

from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtWidgets
from terminal_advisor.gui.qt import main_window, settings_window
from terminal_advisor.gui.threads import Refresh, Run, Search
from terminal_advisor.gui import settings
from terminal_advisor.advisor import Advisor


class GUIApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self, advisor, config):
        super(self.__class__, self).__init__()
        self.advisor = advisor
        self.config = config
        self.setupUi(self)
        self.settings_form = None
        self.run_thread = None
        self.refresh_thread = None
        self.search_thread = None

        # connections
        self.button_refresh.clicked.connect(self.refresh)
        self.button_run.clicked.connect(self.run)
        self.line_edit_advisee.editingFinished.connect(self.advisee_search)
        # self.action_settings.triggered.connect(self.menu_select)
        self.button_settings.clicked.connect(self.menu_select)


    @pyqtSlot()
    def menu_select(self):
        self.settings_form = settings.GUIApp(self.advisor, self.config)
        self.settings_form.show()


    @pyqtSlot()
    def advisee_search(self):
        search_term = self.line_edit_advisee.text()
        self.search_thread = Search(self.advisor, search_term)
        self.search_thread.done.connect(self.refresh_update)
        self.search_thread.start()

    @pyqtSlot()
    def refresh(self):
        self.refresh_thread = Refresh(self.advisor)
        self.refresh_thread.done.connect(self.refresh_update)
        self.refresh_thread.start()

    @pyqtSlot(list)
    def refresh_update(self, advisees):
        self.list_advisees.clear()
        self.list_advisees.addItems(advisees)

    @pyqtSlot()
    def run(self):
        action = str(self.combo_action.currentText())
        advisee = self.list_advisees.currentItem().text()
        self.run_thread = Run(self.advisor, action, advisee)
        self.run_thread.done.connect(self.run_done)
        self.run_thread.start()

    @pyqtSlot(str)
    def run_done(self, msg):
        pass


def main(advisor, no_login, config):
    if advisor.login_ready() and not no_login:
        advisor.login()
    app = QtWidgets.QApplication(sys.argv)
    form = GUIApp(advisor, config)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    advisor = Advisor()
    main(None)

