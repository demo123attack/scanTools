from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Twist\req.xlsx')
sheet = xl.add_worksheet('sheet1')


url="https://developer.twist.com/v3/#get-comment"

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)


allreq=soup.find_all("pre")

i=0

for r in allreq:
    sheet.write_string(i,0,r.get_text())
    i=i+1
    print(i)

xl.close()
