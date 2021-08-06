from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import xlsxwriter



url = pd.read_table('facebook_url.txt',header = None)
browser = webdriver.Chrome()


for i in range(0,len(url)):
    browser.get(url[0][i])
    h4 = browser.find_elements(By.CSS_SELECTOR,'._4-u2._57mb._1u44._3fw6._4-u8._3la3 h4')
    for h in h4:
        print(h.text)




