from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Clip\api_description.xlsx')
sheet = xl.add_worksheet('sheet1')

url = 'https://www.zoho.com/cliq/help/restapi/v2/#add-user'

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

# allname = soup.find_all('h2')
# for i in range(19, len(allname)):
#     print(allname[i].get_text())


url = soup.find_all(name="pre", attrs={"class": "prettyprint"})
for i in range(20, len(url)):
    print(url[i].find_next("p").get_text())
    # sheet.write_string(i-20, 0, url[i].next_sibling.next_sibling.next_sibling.next_sibling.get_text())

xl.close()