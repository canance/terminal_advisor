#!/usr/bin/env python3

# source: https://nikolak.com/pyqt-qt-designer-getting-started/

import sys

from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtWidgets
from terminal_advisor.gui.qt import main_window, settings_window
from terminal_advisor.gui.threads import Refresh, Run, Search


class GUIApp(QtWidgets.QMainWindow, main_window.Ui_MainWindow):

    def __init__(self, advisor):
        super(self.__class__, self).__init__()
        self.advisor = advisor
        self.setupUi(self)

        # connections
        self.button_refresh.clicked.connect(self.refresh)
        self.button_run.clicked.connect(self.run)
        self.line_edit_advisee.editingFinished.connect(self.advisee_search)

    @pyqtSlot()
    def advisee_search(self):
        search_term = self.line_edit_advisee.text()
        search_thread = Search(self.advisor, search_term)
        search_thread.done.connect(self.refresh_update)
        search_thread.start()

    @pyqtSlot()
    def refresh(self):
        refresh_thread = Refresh(self.advisor)
        refresh_thread.done.connect(self.refresh_update)
        refresh_thread.start()

    @pyqtSlot(list)
    def refresh_update(self, advisees):
        self.list_advisees.clear()
        self.list_advisees.addItems(advisees)

    @pyqtSlot()
    def run(self):
        action = str(self.combo_action.currentText())
        advisee = self.list_advisees.currentItem().text()
        run_thread = Run(self.advisor, action, advisee)
        run_thread.done.connect(self.run_done)
        run_thread.start()

    @pyqtSlot(str)
    def run_done(self, msg):
        pass


def main(advisor):
    app = QtWidgets.QApplication(sys.argv)
    form = GUIApp(advisor)
    form.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main(None)

