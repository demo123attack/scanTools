from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

url = pd.read_table('url.txt',header = None)

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Teams\req_res.xlsx')
sheet = xl.add_worksheet('sheet1')

for i in range(0,165):
    print(i)
    page = urllib.request.urlopen(url[0][i])
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    req = soup.find(name="section", attrs={"id":"tabpanel_1_http"})
    if req == None:
        continue
    sheet.write_string(i,0,req.text)

    div = req.parent#.find_next_sibling('div')
    response = div.find_next_sibling('pre')
    sheet.write_string(i,1,response.text)

xl.close()

