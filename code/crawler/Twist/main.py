from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


# uu = pd.read_table('api_name.txt',header = None)
#
#
# xl = xlsxwriter.Workbook(r'E:\PycharmProjects\webex_api\url.xlsx')
# sheet = xl.add_worksheet('sheet1')

url="https://developer.twist.com/v3/#get-comment"

page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

# allh2 = soup.find_all("h2")
#
# for h in allh2:
#     hh = h.string
#     print(hh)

allp=soup.find_all("p")

for pp in allp:
    c=pp.find("code","prettyprint")
    if c!=None:
        print(c.string)








    # for t in alldiv:
    #     type = t.select('span')[0].string
    #     print(type)







# for u in alldiv:
#     url = u.find('a').string
#     print(url)



# for po in post:
#     print(po)
#
# for p in put:
#     print(p)
#
# for d in delete:
#     print(d)

#
# sheet.write_string(0, 0, 'Methods')
# sheet.write_string(0, 1, 'Description')
#
#
# j = 1
#
#
# for i in range(0,470,2):
#
#     # print(soup.select('td')[i].string)
#     sheet.write_string(j, 0, soup.select('td')[i].string)
#     sheet.write_string(j, 1, soup.select('td')[i+1].string)
#     j = j + 1
#
# xl.close()
#



# arg = soup.find_all('span', attrs={"class": "arg_example"})
# des = soup.find(name="div", attrs={"class": "method_arguments full_width"}).find_all('p')
# res = soup.find_all('span', attrs={"class": "arg_requirement"})



