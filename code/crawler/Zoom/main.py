from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd
import numpy as np

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\zoom\api_p.xlsx')
sheet = xl.add_worksheet('sheet1')

url = pd.read_table('zoom_url.txt',header = None)


for i in range(0,len(url)):
    print(i)
    string_p = ''
    page = urllib.request.urlopen(url[0][i])
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    allp = soup.find('div','HubBlock HubBlock--text flex is-viewing is-padded').find_all('p')
    for p in allp:
        string_p = string_p + p.get_text()

    sheet.write_string(i, 0, string_p)

xl.close()



