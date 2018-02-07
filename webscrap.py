#Importing libraries
import urllib.request as ul
from pandas import read_csv, DataFrame, errors
from bs4 import BeautifulSoup as BS

#getting html
def collect_data():
    url = 'http://www.fakepersongenerator.com/fake-identity-generator?new=refresh'
    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
    req = ul.Request(url, headers = headers)
    resp = ul.urlopen(req)
    soup = BS(resp, 'html.parser')
    html = list(soup.children)[3]
    return html
#creating header
def csv_header(html):
    heads = []
    for head in html.find_all('span'):
        try:
            heads.append(list(head.children)[0])
        except:
            csv_header(collect_data())
            print ('error')
    return heads
#creating data
def row_data(html):
    row = []
    for col in html.find_all(['input', 'p']):
        try:
            temp = col['value'].replace(u'\xa0', ' ')
            row.append(temp)
        except:
            temp = list(col.children)[0]
            row.append(temp)
    return row

data = []
n = int(input("Enter the number of entries: "))
for i in range(n):

    html = collect_data()
    data.append(row_data(html))
try:
    file = open('Data.csv', 'a')
    dataset = read_csv('Data.csv')
    df = DataFrame(data)
    df.to_csv(file, header = False, index=False)
    
except errors.EmptyDataError:
    
    df = DataFrame(data, columns = csv_header(html))
    df.reset_index()
    df.to_csv(file, index= False )  
file.close()
