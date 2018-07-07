import requests
import xml.etree.ElementTree as ET
import pandas as pd
import datetime

date = datetime.datetime.now()
date = date.strftime("%Y%m%d")
#date = "20180522"
url_pattern = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date='
url = url_pattern+date
r = requests.get(url)

with open("curr.xml", "wb") as f:
    f.write(r.content)

tree = ET.parse("curr.xml")
root = tree.getroot()

df = pd.DataFrame(columns=('r030', 'txt', 'rate', 'cc', 'exchangedate'))
obj = root.getchildren()
print(len(obj))

for i in range(0, len(obj)-1):
    obj = root.getchildren()[i].getchildren()
    row = dict(zip(['r030', 'txt', 'rate', 'cc', 'exchangedate'], [obj[0].text, obj[1].text, obj[2].text, obj[3].text, obj[4].text]))
    row_s = pd.Series(row)
    row_s.name = i
    df = df.append(row_s)

file_name = "NBU_currency_"+date+".csv"
df.to_csv(file_name, index=False)
