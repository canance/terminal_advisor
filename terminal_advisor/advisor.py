#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Automate mundane tasks in Webadvisor."""

import os.path
import time
import sys
import re
import os
import pdfkit
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
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
        finally:
            self.accept_next_alert = True
    
    def tearDown(self):
        """ Selenium generated method. """
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
