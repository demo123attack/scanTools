from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd
import re


url = pd.read_table('url.txt',header = None)

xl = xlsxwriter.Workbook(r'E:\本科毕设\CODE\code_rocketChat\api_arguments.xlsx')
sheet = xl.add_worksheet('sheet1')

for i in range(0, 1):
    print(url[0][i])
    page = urllib.request.urlopen(url[0][i])
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    print(i)
    table = soup.find("table")
    print(table[1])


    # http_req = soup.find(name="code", attrs={"class": "lang-http"})
    # sheet.write_string(i, 1, http_req.string)
    # sheet.write_string(i, 2, name.string)
    #
    # desc = soup.find("p", text=re.compile(r'Namespace: microsoft.graph')).next_sibling.next_sibling
    # sheet.write_string(i, 3, desc.get_text())

xl.close()