from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By

import json
if __name__ == '__main__':
  driver = webdriver.Chrome()
  driver.maximize_window()
  driver.get('https://weibo.com/login.php')
  sleep(6)
  driver.find_element(By.XPATH,'//*[@id="pl_login_form"]/div/div[1]/div/a[2]').click()
  sleep(60)#You can modify this waiting time for login, better to use SMS
  dictCookies = driver.get_cookies() 
  jsonCookies = json.dumps(dictCookies) 
  with open('wb_cookies.txt', 'w') as f:
    f.write(jsonCookies)
  print('cookies saved!')
  driver.close()
  driver.quit()
