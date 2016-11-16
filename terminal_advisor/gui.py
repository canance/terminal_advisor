#!/usr/bin/env python3

# source: https://nikolak.com/pyqt-qt-designer-getting-started/

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import pyqtSlot
import sys
from terminal_advisor import mainwindow
from terminal_advisor.advisor import Advisor
from terminal_advisor.threads import Refresh, Run, Search


class GUIApp(QtWidgets.QMainWindow, mainwindow.Ui_MainWindow):

    def __init__(self, advisor):
        super(self.__class__, self).__init__()
        self.advisor = advisor
        self.setupUi(self)

        # connections
        self.buttonRefresh.clicked.connect(self.refresh)
        self.buttonRun.clicked.connect(self.run)
        self.txtAdviseeSearch.editingFinished.connect(self.advisee_search)

    @pyqtSlot()
    def advisee_search(self):
        search_term = self.txtAdviseeSearch.text()
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
        self.listWidgetAdvisees.clear()
        self.listWidgetAdvisees.addItems(advisees)

    @pyqtSlot()
    def run(self):
        action = str(self.comboAction.currentText())
        advisee = self.listWidgetAdvisees.currentItem().text()
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

