from config import *
from functions import *

soup = scrapBaseUrl(BASE_URL_1)

table = soup.find("table", class_=TABLE_CLASS_1)
thead = table.find("thead")
trs = table.find_all("tr")

for th in thead:
    print(th.string)

for tr in trs:
    for td in tr:
        print(td.string)