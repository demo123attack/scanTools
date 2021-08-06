from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


ip = pd.read_table('url.txt',header = None)


xl = xlsxwriter.Workbook(r'E:\PycharmProjects\webex_api\api_argument.xlsx')
sheet = xl.add_worksheet('sheet1')

j = 1
k = 1
i = 1

for m in range(0,34):
    print(m)
    url = ip[0][m]
    print(ip)

    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    alldiv = soup.find_all(name="div", attrs={"class": "_946459efb27637a08ffb2928cc757411-scss"})


    sheet.write_string(j,0,ip[0][m])

    for u in alldiv:
        ur = u.find('a').string
        sheet.write_string(j, 1, ur)
        j = j+1
        print(url)


    for t in alldiv:
        type = t.select('span')[0].string
        sheet.write_string(k, 2, type)
        k = k+1
        print(type)


    for d in alldiv:
        dec = d.select('span')[1].string
        sheet.write_string(i, 3, dec)
        i = i+1
        print(dec)

xl.close()


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



