from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


url = "https://docs.microsoft.com/en-us/graph/api/resources/channel?view=graph-rest-1.0"


page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

td = soup.find_all(name="td", attrs={"style":"text-align: left;"})

# for i in range(2, len(td), 3):
#     print(td[i].get_text())


for i in range(0, len(td), 3):
    a = td[i].find("a")
    if ( a != None ):
        print(a.attrs['href'])
    else:
        print(None)
