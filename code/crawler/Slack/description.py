from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


xl = xlsxwriter.Workbook(r'E:\PycharmProjects\slack_api\api_description.xlsx')
sheet = xl.add_worksheet('sheet1')

url = 'https://api.slack.com/methods/'
page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)



sheet.write_string(0, 0, 'Methods')
sheet.write_string(0, 1, 'Description')


j = 1


for i in range(0,470,2):

    # print(soup.select('td')[i].string)
    sheet.write_string(j, 0, soup.select('td')[i].string)
    sheet.write_string(j, 1, soup.select('td')[i+1].string)
    j = j + 1

xl.close()




