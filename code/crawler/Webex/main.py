from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd

ip = pd.read_table('url.txt',header = None)

xl = xlsxwriter.Workbook(r'E:\PycharmProjects\webex_api\argument.xlsx')
sheet = xl.add_worksheet('sheet1')

j=1


for m in range(0,133):
    url = ip[0][m]
    print(m)


    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    allli = soup.find_all(name="li", attrs={"class": "parameters-item clearfix"})



    sheet.write_string(j, 1, ip[0][m])

    i=2
    for li in allli:

        argument = li.find(name="span", attrs={"class": "_9d5518a7d7f0c13b730c94eef63d0e60-scss"})
        sheet.write_string(j, i, argument.string)
        i = i + 1

        arg_req = li.find(name="span", attrs={"class": "_034d4cbbf6cfa5362393d291d00dde12-scss"})
        if arg_req != None:
            sheet.write_string(j, i, arg_req.string)
            i = i + 1
        else:
            sheet.write_string(j, i, "Optional")
            i = i + 1

        arg_type = li.find(name="span", attrs={"class": "params-hint a389dadf7ccf6be4cb4c3e2ae34e104a-scss"})
        sheet.write_string(j, i, arg_type.string)
        i = i + 1

        if (li.find("input",placeholder=True)) != None:
            example = li.find("input")
            sheet.write_string(j, i, example['placeholder'])
            i = i + 1
        elif (li.find("textarea",placeholder=True)) != None:
            example = li.find("textarea")
            sheet.write_string(j, i, example['placeholder'])
            i = i + 1
        else:
            sheet.write_string(j, i, "True or False")
            i = i + 1


        arg_des = li.find(name="div", attrs={"class": "params-hint a389dadf7ccf6be4cb4c3e2ae34e104a-scss"})
        sheet.write_string(j, i, arg_des.string)
        i = i+1

    j = j+1

xl.close()









        # arg_type = li.find(name="span", attrs={"class": "params-hint a389dadf7ccf6be4cb4c3e2ae34e104a-scss"})
        #
        # print(arg_type.string)
        #
        # arg_des = li.find(name="div", attrs={"class": "params-hint a389dadf7ccf6be4cb4c3e2ae34e104a-scss"})
        # print(arg_des.string)




        # print(argument.string)

        # if(arg_req != None):
        #     print(arg_req.string)
        # else:
        #     print(None)



