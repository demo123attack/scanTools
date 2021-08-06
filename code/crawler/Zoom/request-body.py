from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import xlsxwriter

xl = xlsxwriter.Workbook(r'request_body-arg-all.xlsx')
sheet = xl.add_worksheet('sheet1')
url = pd.read_table('zoom_url.txt',header = None)
browser = webdriver.Chrome()

for i in range(0, len(url)):
    m = 0
    k = 1
    print(i)
    browser.get(url[0][i])

    arguments = browser.find_elements(By.CSS_SELECTOR, '.HubBlock.HubBlock--accordion.flex.is-viewing.ApiOperation--requestBody.is-padded.is-outlined.is-standalone .JSV-row.JSV-row--1.flex.relative.py-2 .mr-3')
    requireds = browser.find_elements(By.CSS_SELECTOR, '.HubBlock.HubBlock--accordion.flex.is-viewing.ApiOperation--requestBody.is-padded.is-outlined.is-standalone .JSV-row.JSV-row--1.flex.relative.py-2')
    for arg in arguments:
        sheet.write_string(i, m, arg.text)
        m = m + 2
    for one in requireds:
        req = one.find_elements(By.CSS_SELECTOR, '.text-right.text-sm.pr-3.max-w-sm')  # 找每一行的required div，再根据div中的信息判断
        if len(req) > 0:
            if 'required' in req[0].text:
                sheet.write_string(i, k, 'required')
        k = k + 2

xl.close()

browser.close()