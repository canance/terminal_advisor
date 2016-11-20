#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt


def busy(func):
    """ Decorator to change cursor to busy. """
    def decorator(*args, **kwargs):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        QApplication.processEvents()
        print('busy operation...')  # forces cursor change?
        func(*args, **kwargs)
        QApplication.restoreOverrideCursor()

    return decorator
