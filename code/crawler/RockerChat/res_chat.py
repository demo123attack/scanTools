from selenium import webdriver
from selenium.webdriver.common.by import By
import xlsxwriter
import pandas as pd
import re

url = pd.read_table('url.txt',header = None)

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\RockerChat\res1.xlsx')
sheet = xl.add_worksheet('sheet1')

browser = webdriver.Chrome()
for i in range(0,241):
    print(i+1)
    browser.get(url[0][i])
    response = browser.find_elements(By.CSS_SELECTOR, "#example-result+div")
    request = browser.find_elements(By.CSS_SELECTOR, "#example-call+div")
    payload = browser.find_elements(By.CSS_SELECTOR, "#example-payload+div")
    col=0
    for req in request:
        sheet.write_string(i,col,req.text)
        col = col + 1
    for res in response:
        sheet.write_string(i,col,res.text)
        col = col + 1
    for p in payload:
        sheet.write_string(i,col,p.text)
        col = col + 1
xl.close()

browser.close()
