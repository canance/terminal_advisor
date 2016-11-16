from PyQt5.QtCore import QThread, pyqtSignal

from terminal_advisor.advisor import Advisor

advisee_list = []


class Refresh(QThread):
    done = pyqtSignal(list)

    def __init__(self, advisor):
        QThread.__init__(self)
        self.advisor = advisor

    def __del__(self):
        self.wait()

    def run(self):
        global advisee_list
        advisee_list = self.advisor.list_advisees()
        self.done.emit(advisee_list)


class Run(QThread):

    done = pyqtSignal(str)
    program_evaluation = 'Program Evaluation'
    remove_hold = 'Remove Advisor Hold'

    def __init__(self, advisor, action, advisee):
        QThread.__init__(self)
        self.advisor = advisor
        self.action = action
        self.advisee = advisee

    def __del__(self):
        self.wait()

    def run(self):
        msg = 'Done'
        if self.action == self.program_evaluation:
            self.advisor.run_program_evaluation(self.advisee)
        elif self.action == self.remove_hold:
            self.advisor.remove_advisor_hold(self.advisee)
        else:
            msg = 'Unsupported action [%s].' % self.action
        self.done.emit(msg)


class Search(QThread):

    done = pyqtSignal(list)

    def __init__(self, advisor, search_term):
        QThread.__init__(self)
        self.advisor = advisor
        self.search_term = search_term

    def __del__(self):
        self.wait()

    def run(self):
        global advisee_list
        results = []
        for advisee in advisee_list:
            if self.search_term.lower() in advisee.lower():
                results.append(advisee)
        self.done.emit(results)

