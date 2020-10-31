from functions import *
from config import *

# Scraps table from BASE_URL_1
soup = scrapBaseUrl(BASE_URL_1 + PATH_1)
table = soup.find("table", class_=TABLE_CLASS_1)

# Opens csv file
f = codecs.open(OUTPUT_FILE_1, "w", "utf-8")

# Builds and writes excel's head
excel_head = getExcelHead(table, THEAD_PRODUCT_1)
f.write(excel_head)

# Builds and writes excel's data
for tr in table.find_all("tr"):
    excel_row = getExcelRow_1(tr)
    f.write(excel_row)

# Close csv file
f.close()