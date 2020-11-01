from func_pcpcanada import *

# Scraps table from BASE_URL
soup = scrapBaseUrl(BASE_URL + PATH)
table = soup.find("table", class_=TABLE_CLASS)

# Opens csv file

f = codecs.open(getAbsolutePath(OUTPUT_FILE), "w", "utf-8")

# Builds and writes excel's head
excel_head = getExcelHead(table, THEAD_PRODUCT)
f.write(excel_head)

# Builds and writes excel's data
for tr in table.find_all("tr"):
    excel_row = getExcelRow(tr)
    f.write(excel_row)

# Close csv file
f.close()