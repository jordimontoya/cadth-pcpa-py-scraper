import requests
from bs4 import BeautifulSoup
import codecs
from config import *

def scrapBaseUrl(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')

# Returns excel columns' head as a string
def getExcelHead(table, arr_head):
    thead = [e.text for e in table.find("thead").find_all("th")]
    return SEPARATOR.join(thead) + '|url|' + SEPARATOR.join(arr_head) + '\n'

# Returns excel row as a string
def getExcelRow_1(tr):
    table_row = SEPARATOR.join( [e.get_text(separator=" ").strip() for e in tr.find_all("td")] )
    print(table_row + '\n')

    url_product = BASE_URL_1 + '' + tr.td.a['href']
    soup = scrapBaseUrl("https://www.cadth.ca/pembrolizumab-keytruda-hnscc-details")
    product_detail = getProductDetail_1(soup)

    return table_row + '|' + url_product + '|' + product_detail + '\n'

# Returns the detail row as a string
def getProductDetail_1(soup):
    row = ''

    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    #2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
    if soup.find("table", class_=TABLE_PRODUCT_CLASS_1):

        product_tr_list = soup.find("table", class_=TABLE_PRODUCT_CLASS_1)
        product_row = []

        for element in THEAD_PRODUCT_1:
            if product_tr_list.find("th", string=element):
                string = product_tr_list.find("th", string=element).find_next_sibling("td").get_text(separator=" ").strip()
                string = string.replace('\n', ' ').replace('\r', '')
                product_row.append(string)
            else:
                product_row.append("")

        row = SEPARATOR.join(product_row)

    #3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)    
    elif soup.find("div", class_="publish-date"):
        for element in THEAD_PRODUCT_1:
            
            if element == "Manufacturer":
                #clean manufacturer value
                manufacturer = soup.find("p", class_="field_manufacturer")
                manufacturer.strong.decompose()
                row = row + manufacturer.get_text(separator=" ").strip()
            
            elif element == "Submission Type" and soup.find("p", class_="field_submission_type"):
                #clean submission type value
                submission_type = soup.find("p", class_="field_submission_type")
                submission_type.strong.decompose()
                row = row + submission_type.get_text(separator=" ").strip()
            else:
                row = row + "|"

    else:
        row = "Unable to fetch data, new web format"

    return row