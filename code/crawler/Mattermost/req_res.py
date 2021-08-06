from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter

url = 'https://api.mattermost.com/#tag/users'

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Mattermost\response.xlsx')
sheet = xl.add_worksheet('sheet1')

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

h3 = soup.find_all('h3',text=" Response samples ")
col = 0
for h in h3:
    div = h.find_next_sibling()
    req = div.find(name="div", attrs={"class": "redoc-json"})
    if(req!=None):
        sheet.write_string(col, 0, req.get_text())
    col = col + 1


xl.close()

