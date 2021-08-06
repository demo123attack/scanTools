from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


url = 'https://api.mattermost.com/#tag/users'

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\Mattermost\test.xlsx')
sheet = xl.add_worksheet('sheet1')


page = urllib.request.urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html)

alldiv = soup.find_all(name="div", attrs={"class": "sc-RefOD boajtD"})

j=1
for div in alldiv:
    d = div.find('p').get_text()
    sheet.write_string(j, 1, d)
    j = j + 1

xl.close()




# for type in alltype:
#     t = type.find('span')
#     print(t.get_text())




# i=1
# for url in allurl:
#     uu = url.get_text()
#     if i%2==0: # == or !=
#         print(uu)
#     i = i+1




# for h in allh2:
#     name = h.string
#     print(h)

# for t in alldiv:
#     type = t.select('span')[0].string
#     sheet.write_string(k, 2, type)
#     k = k+1
#     print(type)
#
#
# for d in alldiv:
#     dec = d.select('span')[1].string
#     sheet.write_string(i, 3, dec)
#     i = i+1
#     print(dec)



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



