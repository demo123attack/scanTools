from bs4 import BeautifulSoup
import urllib.request
import xlsxwriter
import pandas as pd


u = pd.read_table('api.txt',header = None)



xl1 = xlsxwriter.Workbook(r'E:\PycharmProjects\slack_api\api_arg.xlsx')
xl2 = xlsxwriter.Workbook(r'E:\PycharmProjects\slack_api\api_example.xlsx')
xl3 = xlsxwriter.Workbook(r'E:\PycharmProjects\slack_api\api_description.xlsx')

sheet1 = xl1.add_worksheet('sheet1')
sheet2 = xl2.add_worksheet('sheet1')
sheet3 = xl3.add_worksheet('sheet1')



for m in range(0,234):

    url = 'https://api.slack.com/methods/'+u[0][m]
    # print(url)
    page = urllib.request.urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html)

    mm=m+1

    sheet1.write_string(mm, 0, u[0][m])
    sheet2.write_string(mm, 0, u[0][m])
    sheet3.write_string(mm, 0, u[0][m])



    print(mm)

    j=1
    x=1
    k=1
    arg = soup.find_all('span', attrs={"class": "arg_example"})
    des = soup.find(name="div", attrs={"class": "method_arguments full_width"}).find_all('p')
    res = soup.find_all('span', attrs={"class": "arg_requirement"})

    for a in arg:
        # print(a.get_text())
        sheet1.write_string(mm, j, a.get_text())
        j = j + 3

    for d in des:
        # print(d.get_text())
        sheet2.write_string(mm, x, d.get_text())
        x = x + 2

    for r in res:
        # print(r.get_text())
        sheet3.write_string(mm, k, r.get_text())
        k = k + 2


xl1.close()
xl2.close()
xl3.close()



