#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import logging
import os
import sys
from datetime import date, datetime, timedelta
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pause

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler(os.getcwd() + os.sep + "log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(handler)
logger.addHandler(console)

browser = webdriver.Chrome()
browser.maximize_window()
browser.get('https://weibo.com/login.php')


class sendingDM:
    def __init__(self, config):
        self.uid = config['uid']
        self.msg = config['msg']
        self.clock = config['clock']
        self.cookie_path = config['cookie_path']
        
        print('UID : ', self.uid)
        print('MSG : ', self.msg)
        print('CLOCK : ', self.clock)
        if self.cookie_path == "": #if none -> in the same path
            self.cookie_path = 'wb_cookies.txt'
        print('COOKIE : ', self.cookie_path)

    def log_csdn(self, browser):
        with open(self.cookie_path, 'r', encoding='utf8') as f:
            listCookies = json.loads(f.read())

        # add cookie to browser
        for cookie in listCookies:
            cookie_dict = {
                'domain': '.weibo.com',
                'name': cookie.get('name'),
                'value': cookie.get('value'),
                "expires": '',
                'path': '/',
                'httpOnly': False,
                'HostOnly': False,
                'Secure': False
            }
            browser.add_cookie(cookie_dict)
        sleep(10)#You can modify this waiting time
        browser.refresh()  # fresh to validate cookie

    def find_uid(self, browser):
        url = 'https://weibo.com/u/' + self.uid
        browser.get(url)
        sleep(5)

    def send_dm(self, browser):   
        browser.find_element(By.XPATH,'//*[@id="app"]/div[1]/div[2]/div[2]/main/div/div/div[2]/div[1]/div[1]/div[2]/a/button').click()
        sleep(5)    
        # get multiple window
        windows = browser.window_handles
        # switch to new DM window
        browser.switch_to.window(windows[-1])    
        sleep(3)
    
    def dm_detail(self, browser):
        #print(browser.current_url)
        dm = browser.find_element(By.XPATH,'//*[@id="webchat-textarea"]')
        dm.send_keys(self.msg)
        return dm, browser 
    
    def dm_enter(self, browser, dm):
        dm.send_keys(Keys.ENTER)
        #be careful of the delay
        #print(datetime.now())
    
    def start(self,browser):
        try:
            #browser = self.browser_initial()
            sleep(5)
            self.log_csdn(browser)
            self.find_uid(browser)
            self.send_dm(browser)
            dm, browser = self.dm_detail(browser)

            if '~' in self.clock:
                set_time = self.clock
                auto_time = set_time #'2012-05-29 19~30'
                auto_time += '~00.000000'
            else: #don't set minute or hour -> 10 seconds after run the program
                logger.warn('You have not set the time!\nProgram will run after 10s for test')
                now_time = datetime.now() #.strftime('%H:%M:%S')
                set_time = now_time + timedelta(seconds=10)
                set_time = set_time.strftime("%Y-%m-%d %H~%M~%S")#string
                auto_time = set_time #'2012-05-29 19:30:03'
                auto_time += '.000000'
            
            auto_time = datetime.strptime(auto_time, "%Y-%m-%d %H~%M~%S.%f")
            #print(auto_time)
            #2023-02-11 15:10.000000
        
            pause.until(auto_time)
            self.dm_enter(browser, dm)
            #nowtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        except Exception as e:
            logger.exception(e)
            #logger.info('*' * 100 + '\n')     

def _get_config():
    """get dm.json"""
    config_path = os.getcwd() + os.sep + 'dm.json'
    try:
        with open(config_path) as f:
            config = json.loads(f.read())
            return config
    except ValueError:
        logger.error(u'dm.json Format Error')
        sys.exit()

if __name__ == '__main__':
    try:
        config = _get_config()
        wbDM = sendingDM(config)
        wbDM.start(browser)
        logger.info('Finished\n')
    except Exception as e:
        logger.exception(e)
        logger.info('\n')