from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Clip\api_argument.xlsx')
sheet = xl.add_worksheet('sheet1')

url = 'https://www.zoho.com/cliq/help/restapi/v2/#add-user'

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

paraments = soup.find_all(name='div', attrs={'class': 'parameter'})

row = 0
for m in range(4, len(paraments)):
    coll = 0
    colr = 2
    left = paraments[m].find_all(name='div', attrs={'class': 'left'})
    for l in left:
        sheet.write_string(row, coll, l.get_text())
        coll = coll + 1
        sheet.write_string(row, coll, l.get_text())
        coll = coll + 3

    right = paraments[m].find_all(name='div', attrs={'class': 'right'})
    for r in right:
        div = r.find_all('div')
        sheet.write_string(row, colr, div[0].get_text())
        colr = colr + 1
        sheet.write_string(row, colr, div[1].get_text())
        colr = colr + 3

    row = row + 1

xl.close()
