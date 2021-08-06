from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter

url = 'https://api.mattermost.com/#tag/users'

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Mattermost\arg.xlsx')
sheet = xl.add_worksheet('sheet1')

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

alltable = soup.find_all(name="table", attrs={"class": "sc-dxgOiQ eCjbJc"})

for i in range(0,len(alltable)):
    print(i+1)
    coln=0
    colt=2
    cold=3
    arg_name = alltable[i].find_all(name="td", attrs={"class": "sc-cSHVUG sc-chPdSV bIrgla"})
    for name in arg_name:
        sheet.write_string(i,coln,name.get_text())
        coln = coln+1
        sheet.write_string(i, coln, name.get_text()+'222')
        coln = coln+3

    td = alltable[i].find_all(name="td", attrs={"class": "sc-kgoBCf kGwPhO"})
    for t in td:
        type = t.find('div').find('div')
        sheet.write_string(i,colt,type.get_text())
        colt = colt+4

    desc = alltable[i].find_all(name="div", attrs={"class": "sc-jWBwVP sc-iRbamj gDsWLk"})
    for d in desc:
        sheet.write_string(i,cold,d.get_text())
        cold=cold+4

xl.close()

