from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

uu = pd.read_table('url.txt', header=None)

u = "https://docs.rocket.chat/api/rest-api/methods/users/"

n = 241


for m in range(0,n):
    url = u + uu[0][m]
    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)
    name = soup.find(name="title", attrs={"data-react-helmet": "true"})
    print(name.get_text())

# print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
#
# for m in range(0, n):
#     url = u + uu[0][m]
#
#     page = urllib.request.urlopen(url)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html)
#
#     add = soup.select("p")[4]       #url  "0"+add.get_text()
#     print("0"+add.get_text())
#
# print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
# #
# # for m in range(0, n):
#     url = u + uu[0][m]
#     page = urllib.request.urlopen(url)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html)
#
#     HTTP = soup.select("p")[6]
#     print(HTTP.get_text())
#
# print("55555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555")
#
# for m in range(0, n):
#     url = u + uu[0][m]
#
#     page = urllib.request.urlopen(url)
#     html = page.read().decode("utf-8")
#     soup = BeautifulSoup(html)
#
#     desc = soup.find("p","blockParagraph-544a408c")
#     if desc == None:
#         print(None)
#     else:
#         print(desc.get_text())
#
#





#     sheet.write_string(j,0,uu[0][m])
#
#     for u in alldiv:
#         ur = u.find('a').string
#         sheet.write_string(j, 1, ur)
#         j = j+1
#         print(url)
#
#
#     for t in alldiv:
#         type = t.select('span')[0].string
#         sheet.write_string(k, 2, type)
#         k = k+1
#         print(type)
#
#
#     for d in alldiv:
#         dec = d.select('span')[1].string
#         sheet.write_string(i, 3, dec)
#         i = i+1
#         print(dec)
#
# xl.close()


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



