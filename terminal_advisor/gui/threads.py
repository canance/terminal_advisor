from PyQt5.QtCore import QThread, pyqtSignal

from terminal_advisor.advisor import Advisor
import os
import configparser
import keyring

advisee_list = []

# ---------------------------------------------------- main.py threads


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

# ---------------------------------------------------- settings.py threads


class Login(QThread):

    done = pyqtSignal()

    def __init__(self, advisor, base_url, user_name, password):
        QThread.__init__(self)
        self.advisor = advisor
        self.base_url = base_url
        self.user_name = user_name
        self.password = password

        def __del__(self):
            self.wait()

        def run(self):
            pass


class Save(QThread):

    done = pyqtSignal()

    def __init__(self, advisor, base_url, user_name, password, save_password):
        QThread.__init__(self)
        self.advisor = advisor
        self.base_url = base_url
        self.user_name = user_name
        self.password = password
        self.save_password = save_password

        def __del__(self):
            self.wait()

        def run(self):
            pass

        def parse_config(**kwargs):
            """ Setup configuration for program.  This function will also read or create a configuration file. """
            config_path = 'config.ini', os.path.join(os.path.expanduser('~'), '.terminal_advisor', 'config.ini')
            config = configparser.ConfigParser()
            config.read(config_path)
            if len(config.sections()) == 0:  # make config
                config['DEFAULT'] = {
                    'User': '',
                    'WebadvisorURL': '',
                    'Driver': '',
                }
                config['KEYRING'] = {
                    'Use': 'false',
                    'Keychain': 'terminaladvisor-webadvisor',
                }


            config['DEFAULT']['User'] = kwargs['user']
            config['DEFAULT']['WebadvisorURL'] = kwargs['base_url']
            config['DEFAULT']['Driver'] = kwargs['driver']
            config['KEYRING']['Use'] = kwargs['save_password']


            password = ''
            if config.getboolean('KEYRING', 'Use'):
                password = keyring.get_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'])

            if kwargs['save_password'] and len(kwargs['password'].strip()) > 0:
                keyring.set_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'], password)

            if not os.path.exists(os.path.split(config_path)[0]):
                os.mkdir(os.path.split(config_path)[0])
                with open(config_path, 'w') as configfile:
                    config.write(configfile)

            return config