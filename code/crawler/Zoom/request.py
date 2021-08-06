from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import xlsxwriter

xl = xlsxwriter.Workbook(r'request-body-example.xlsx')
sheet = xl.add_worksheet('sheet1')
url = pd.read_table('zoom_url.txt',header = None)
browser = webdriver.Chrome()

for i in range(0, len(url)):
    print(i)
    browser.get(url[0][i])
    buttons = browser.find_elements(By.CSS_SELECTOR,
    '.HubBlock.HubBlock--accordion.flex.is-viewing.ApiOperation--requestBody.is-padded.is-outlined.is-standalone .dropdown.icon')
    if (len(buttons) == 0):
        continue
    par = browser.find_elements(By.CSS_SELECTOR,
    '.HubBlock.HubBlock--accordion.flex.is-viewing.ApiOperation--requestBody.is-padded.is-outlined.is-standalone .dropdown.icon+div')
    k = 0
    for k in range(0, len(buttons)):
        if 'Example' in par[k].text:
            buttons[k].click()
            break
    if 'Example' not in par[k].text:
        continue
    requests = browser.find_elements(By.CSS_SELECTOR,
                                      '.HubBlock.HubBlock--accordion.flex.is-viewing.ApiOperation--requestBody.is-padded.is-outlined.is-standalone .Highlight.line-numbers')
    for req in requests:
        sheet.write_string(i, 0, req.text)

xl.close()

browser.close()