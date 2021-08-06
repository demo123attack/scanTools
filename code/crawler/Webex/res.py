from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

url = pd.read_table('url.txt',header = None)


xl = xlsxwriter.Workbook(r'E:\PycharmProjects\webex_api\res_webex.xlsx')
sheet = xl.add_worksheet('sheet1')

# resquest  div class     _1fcfc924d62388b60a54bce7c9309142-scss
# response   div classs   _821782ff383876b3fc5daf97af910547-scss _069178c1ac3444f8ba8dd6fb031375a0-scss

for m in range(0,133):
    print(m+1)
    page = urllib.request.urlopen(url[0][m])
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    request = soup.find(name="div", attrs={"class": "_1fcfc924d62388b60a54bce7c9309142-scss"})
    response = soup.find(name="div", attrs={"class": "_821782ff383876b3fc5daf97af910547-scss _069178c1ac3444f8ba8dd6fb031375a0-scss"})

    resquest_josn = soup.find(name="div",attrs={"class":"_821782ff383876b3fc5daf97af910547-scss"})

    if(request != None):
        sheet.write_string(m,0,request.get_text())
    elif(resquest_josn != None):
        sheet.write_string(m,0,resquest_josn.get_text())

    if(response != None):
        sheet.write_string(m,1,response.get_text())

xl.close()
