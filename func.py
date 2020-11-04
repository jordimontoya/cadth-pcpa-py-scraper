import xlsxwriter
import requests
import os
from bs4 import BeautifulSoup
from datetime import datetime
import codecs

OUTPUT_FILE = "output/CADTH-pCPA-data-import.xlsx"
BASE_URL_CADTH = "https://www.cadth.ca"
PATH_CADTH = "/reimbursement-review-reports"
TABLE_CLASS_CADTH = "reimbursement_review"
TABLE_PRODUCT_CLASS_CADTH = "pcodr_table"
THEAD_PRODUCT_CADTH = ["Strength","Tumour Type","Funding Request","Pre Noc Submission","NOC Date","Manufacturer","Sponsor","Submission Deemed Complete","Submission Type","Prioritization Requested","Stakeholder Input Deadline","Check-point meeting","pERC Meeting","Initial Recommendation Issued","Feedback Deadline","pERC Reconsideration Meeting","Notification to Implement Issued","Clarification"]

BASE_URL_PCPA = "https://www.pcpacanada.ca"
PATH_PCPA = "/negotiations"
TABLE_CLASS_PCPA = "datatable"
THEAD_PRODUCT_PCPA = []

def getAbsolutePath(relative_path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_path = os.path.join(script_dir, relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return abs_path

def scrapBaseUrl(url):
    r = requests.get(url)
    return BeautifulSoup(r.text, 'lxml')

def dateParser(str):
    if str and str != 'N/A':
        return datetime.strptime(str, '%B %d, %Y')
    return str

# Returns excel columns' head as array
def getExcelHead(table, arr_head):
    thead = [e.text for e in table.find("thead").find_all("th")]
    return thead + arr_head

# Returns excel row as a string
def getExcelRow(tr):
    table_row = [e.get_text(separator=" ").strip() for e in tr.find_all("td")]

    # product url
    url_product = BASE_URL_CADTH + '' + tr.td.a['href']
    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = scrapBaseUrl(url_product)
    product_row = getProductDetail(soup)
    print(product_row)

    return table_row + product_row

# Returns the detail row as a string
def getProductDetail(soup):
    product_row = []

    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    #2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
    if soup.find("table", class_=TABLE_PRODUCT_CLASS_CADTH):
        product_tr_list = soup.find("table", class_=TABLE_PRODUCT_CLASS_CADTH)
        product_row = [parseProductTable(element, product_tr_list) for element in THEAD_PRODUCT_CADTH]

    #3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)    
    elif soup.find("div", class_="publish-date"):
        product_row = [cleanProductElement(element, soup) for element in THEAD_PRODUCT_CADTH]
    else:
        product_row.append("Unable to fetch data, new web format")

    return product_row

def parseProductTable(element, product_tr_list):
    if product_tr_list.find("th", string=element):
        product_td = product_tr_list.find("th", string=element).find_next_sibling("td").get_text(separator=" ").strip()
        product_td = product_td.replace('\n', ' ').replace('\r', '')
        return product_td

    return ""

def cleanProductElement(element, soup):
    if element == "Manufacturer":
        #clean manufacturer value
        manufacturer = soup.find("p", class_="field_manufacturer")
        manufacturer.strong.decompose()
        return manufacturer.get_text(separator=" ").strip()

    elif element == "Submission Type" and soup.find("p", class_="field_submission_type"):
        #clean submission type value
        submission_type = soup.find("p", class_="field_submission_type")
        submission_type.strong.decompose()
        return submission_type.get_text(separator=" ").strip()

    return ""