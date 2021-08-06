from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import re

url = pd.read_table('url.txt',header = None)


browser = webdriver.Chrome()
for i in range(0,241):
    browser.get(url[0][i])
    div = browser.find_elements(By.CSS_SELECTOR, "div.reset-3c756112--codeBlockWrapper-56f27afc")
    if(len(div)!=2):
        print(i+1)
        print(url[0][i])