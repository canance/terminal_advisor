#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Automate mundane tasks in Webadvisor."""
import argparse
import getpass
import os.path
import time
import sys
import re
import os
import configparser
import keyring
import pdfkit
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup


__author__ = "Cory Nance"
__copyright__ = "Copyright 2016"
__credits__ = ["Cory Nance"]
__license__ = "MIT"
__version__ = "1.1"
__maintainer__ = "Cory Nance"
__email__ = "canance@coastal.edu"
__status__ = "Development"

class Advisor:
    """ Class to interact with webadvisor """
    
    def __init__(self, base_url, username, password, driver='PhantomJS'):
        """ Setup instance variables for Advisor and login to webadvisor. """
        if driver == 'PhantomJS':
            self.driver = webdriver.PhantomJS(service_log_path=os.path.devnull)
        elif driver == 'Chrome':
            self.driver = webdriver.Chrome(service_log_path=os.path.devnull)
        elif driver == 'Firefox':
            self.driver = webdriver.Firefox(service_log_path=os.path.devnull)
        else:
            print('[*ERROR] Unknown driver: %s' % driver)
            sys.exit(1)
        self.driver.implicitly_wait(30)
        self.base_url = base_url
        self.verificationErrors = []
        self.accept_next_alert = True
        self.username = username
        self.password = password
        self.login()

    def login(self):
        """ Login to webadvisor. """
        driver = self.driver
        driver.get(self.base_url + "/")
        driver.find_element_by_css_selector("#acctLogin > a > span.label").click()
        driver.find_element_by_id("USER_NAME").clear()
        driver.find_element_by_id("USER_NAME").send_keys(self.username)
        driver.find_element_by_id("CURR_PWD").clear()
        driver.find_element_by_id("CURR_PWD").send_keys(self.password)
        driver.find_element_by_name("SUBMIT2").click()


    def advisee_search(self, advisee):
        """ Search for an advisee. """

        print("Searching for %s..." % advisee)
        driver = self.driver
        driver.find_element_by_link_text("Faculty").click()
        driver.find_element_by_xpath("//div[@id='bodyForm']/div[3]/div[2]/ul[2]/li[2]/a/span").click()
        driver.find_element_by_id("DATE_VAR1").clear()
        today = time.strftime("%m/%d/%Y")
        driver.find_element_by_id("DATE_VAR1").send_keys(today)
        driver.find_element_by_id("DATE_VAR2").clear()
        driver.find_element_by_id("DATE_VAR2").send_keys(today)
        driver.find_element_by_name("SUBMIT2").click()
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        found = False
        row_num = -1
        stu_name = None 
        stu_id = None
        possible_matches = []
        if advisee.isnumeric(): # search by id
            for p in soup.find_all('p', {'id': re.compile('^LIST_VAR10_')}):
                if advisee == p.string:
                    row_num = p.attrs['id'].split('_')[-1]
                    stu_name = soup.find(id='LIST_VAR1_%s' % row_num).string
                    stu_id = p.string
                    match = {
                        'row_num': row_num,
                        'stu_name': stu_name,
                        'stu_id': stu_id,
                    }
                    possible_matches.append(match)          
        else: # search by name
            for p in soup.find_all('p', {'id': re.compile('^LIST_VAR1_')}):
                if advisee.lower() in p.string.lower():
                    row_num = p.attrs['id'].split('_')[-1]
                    stu_id = soup.find(id='LIST_VAR10_%s' % row_num).string
                    stu_name = p.string
                    match = {
                        'row_num': row_num,
                        'stu_name': stu_name,
                        'stu_id': stu_id,
                    }
                    possible_matches.append(match)

        if len(possible_matches) == 0:
            match = None
        elif len(possible_matches) == 1:
            match = possible_matches[0]
        else:
            selection = -1
            for num, match in enumerate(possible_matches):
                print('%d: %s (%s)' % (num+1, match['stu_name'], match['stu_id']))
            print('%d: Exit' % (len(possible_matches) + 1))
            while selection not in range(0, len(possible_matches) + 2):
                selection = int(input('Advisee: '))
            if selection == len(possible_matches) + 1:
                match = None
            else:
                match = possible_matches[selection - 1]
        return match

    
    def run_program_evaluation(self, advisee):
        """ Run a program evaluation for an advisee. """
        advisee = self.advisee_search(advisee)
        driver = self.driver
        if advisee is not None:
            stu_name = advisee['stu_name']
            stu_id = advisee['stu_id']
            row_num = advisee['row_num']
            print("Running program evaluation for %s (%s)..." % (stu_name, stu_id))
            Select(driver.find_element_by_id("LIST_VAR2_%s" % row_num)).select_by_visible_text("EVAL Evaluate Program")
            driver.find_element_by_name("SUBMIT2").click()
            driver.find_element_by_id("LIST_VAR1_1").click()
            driver.find_element_by_name("SUBMIT2").click()
            try:
                delay = 60
                element_present = EC.presence_of_element_located((By.ID, 'FNoteInnerTable'))
                WebDriverWait(driver, delay).until(element_present)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                css = str(soup.find('style'))
                stu_table = str(soup.find(id='StudentTable'))
                html = '<html><head>%s</head><body>%s</body></html>' % (css, stu_table)
                file_name = '%s_%s_eval' % (stu_name, stu_id)
                file_name = file_name.replace('.', '').replace(' ', '_')
                file_name = file_name + '.pdf'
                pdfkit.from_string(html, file_name)
            except TimeoutException:
                print("Webadvisor timed out!")
        

    def remove_advisor_hold(self, advisee):
        """ Remove advisor hold for an advisee. """
        advisee = self.advisee_search(advisee)
        driver = self.driver
        if advisee is not None:
            stu_name = advisee['stu_name']
            stu_id = advisee['stu_id']
            row_num = advisee['row_num']
            print("Removing advising hold for %s (%s)..." % (stu_name, stu_id))
            Select(driver.find_element_by_id("LIST_VAR2_%s" % row_num)).select_by_visible_text("PERC Remove Advisor Hold")
            driver.find_element_by_name("SUBMIT2").click()
            driver.find_element_by_id("VAR9").click()
            driver.find_element_by_name("SUBMIT2").click()
        

    def is_element_present(self, how, what):
        """ Selenium generated method. """
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        """ Selenium generated method. """
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        """ Selenium generated method. """
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        """ Selenium generated method. """
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)


def parse_config(args, config_path=['config.ini', os.path.join(os.environ['HOME'], '.terminal_advisor/config.ini')]):
    """ Setup configuration for program.  This function will also read or create a configuraiton file. """
    config = configparser.ConfigParser()
    if not isinstance(config_path, list):
        config_path = [config_path]
    for path in config_path:
        if os.path.isfile(path):
            config.read(path)
            break
    if len(config.sections()) == 0: # make config
        config['DEFAULT'] = {
            'User': '',
            'WebadvisorURL': '',
            'Driver': '',
        }
        config['KEYRING'] = {
            'Use': 'false',
            'Keychain': 'terminaladvisor-webadvisor',
        }


    if args.user is not None:
        config['DEFAULT']['User'] = args.user
    if args.base_url is not None:
        config['DEFAULT']['WebadvisorURL'] = args.base_url
    if args.driver is not None:
        config['DEFAULT']['Driver'] = args.driver

    if not config['DEFAULT']['User']:
        config['DEFAULT']['User'] = input('Username: ')

    password = ''
    if config.getboolean('KEYRING', 'Use'):
        password = keyring.get_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'])
    if not password:
        password = getpass.getpass('Password: ')
        store = input("Would you like to store this password in your keychain (Y/n): ")
        if store.lower() in ['y', 'yes', '']:
            config['KEYRING']['Use'] = 'true'
            keyring.set_password(config['KEYRING']['Keychain'], config['DEFAULT']['User'], password)
    
    if not config['DEFAULT']['WebadvisorURL']:
        config['DEFAULT']['WebadvisorURL'] = input('Webadvisor base URL: ')
    
    if not config['DEFAULT']['Driver']:
        config['DEFAULT']['Driver'] = 'PhantomJS'
    
    if args.save_config:
        save = input('Save configuration (Y/n)? ')
        if save.lower() in ['y', 'yes', '']:
            ask_path = input('Location (%s): ' % path)
            if ask_path.strip() != '':
                path = ask_path
            if not os.path.exists(os.path.split(path)[0]):
                os.mkdir(os.path.split(path)[0])
            with open(path, 'w') as configfile:
                config.write(configfile)

    return (config, password)


def get_args():
    """ Parse command line arguments. """
    drivers = ['PhantomJS', 'Chrome']
    parser = argparse.ArgumentParser(description='Automate mundane tasks in Webadvisor')
    parser.add_argument('--user', dest='user', help='User name to log in to webadvisor')
    parser.add_argument('--base-url', dest='base_url', help='Base URL for webadvisor.  Example: https://wa.xyz.edu/')
    parser.add_argument('--config', dest='config', help='Path to a configuration file')
    parser.add_argument('--driver', dest='driver', choices=drivers, nargs='?', default='PhantomJS', help='Webdriver to use with Selenium'),
    parser.add_argument('-s', '--save-config', dest='save_config', action='store_true', help='Save configuration file')
    parser.add_argument('-r', '--remove-hold', dest='remove_hold', action='store_true', help='Remove the advisement hold')
    parser.add_argument('-e', '--program-eval', dest='prog_eval', action='store_true', help='Run a program evaluation')
    parser.add_argument('advisee', nargs='?', help="An advisee's name or student ID number.")
    return parser.parse_args()


def main():
    """ Main function.  Parse command-line arguments, load configuration, process commands. """
    args = get_args()
    config, password = parse_config(args)
    
    if args.advisee is not None:
        advisee = args.advisee
    else:    
        advisee = input('Advisee: ')
    
    advisor = Advisor(config['DEFAULT']['WebadvisorURL'], config['DEFAULT']['user'], password, config['DEFAULT']['Driver'])
    
    if args.remove_hold:
        advisor.remove_advisor_hold(advisee)
    elif args.prog_eval:
        advisor.run_program_evaluation(advisee)
    else:    
        print('1. Remove Advisor Hold')
        print('2. Run Program Evaluation')
        print('3. Quit')
        selection = -1
        while selection not in [1, 2, 3]:
            selection = int(input('Choice: '))
        if selection == 1:
            advisor.remove_advisor_hold(advisee)
        elif selection == 2:
            advisor.run_program_evaluation(advisee)
        elif selection == 3:
            sys.exit(0)


if __name__ == '__main__':
    main()
