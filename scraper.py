import requests
import xlsxwriter
import cProfile
import os
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

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

session = requests.Session()
session.trust_env = False

def getAbsolutePath(relative_path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_path = os.path.join(script_dir, relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return abs_path

def scrapBaseUrl(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    r = session.get(url, headers=headers)
    r.raw.chunked = True
    r.encoding = 'utf-8'
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

    excel_row = table_row + product_row

    # Parse dates
    excel_row[5] = dateParser(excel_row[5])
    excel_row[6] = dateParser(excel_row[6])
    excel_row[12] = dateParser(excel_row[12])
    excel_row[15] = dateParser(excel_row[15])
    excel_row[19] = dateParser(excel_row[19])
    excel_row[20] = dateParser(excel_row[20])
    excel_row[22] = dateParser(excel_row[22])
    excel_row[23] = dateParser(excel_row[23])
    excel_row[24] = dateParser(excel_row[24])

    return excel_row

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

def run():
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(getAbsolutePath(OUTPUT_FILE), {'constant_memory': True})
    worksheetCADTH = workbook.add_worksheet('CADTH')
    worksheetPCPA = workbook.add_worksheet('pCPA')

    # Declare specific formats
    bold = workbook.add_format({'bold': True})
    underline = workbook.get_default_url_format()
    date = workbook.add_format({'num_format': 'dd-mmm-yyyy'})

    # CADTH - Set link format
    worksheetCADTH.set_column('A:A', None, underline)

    # CADTH - Set date format
    worksheetCADTH.set_column('F:F', None, date)
    worksheetCADTH.set_column('G:G', None, date)
    worksheetCADTH.set_column('M:M', None, date)
    worksheetCADTH.set_column('P:P', None, date)
    worksheetCADTH.set_column('T:T', None, date)
    worksheetCADTH.set_column('U:U', None, date)
    worksheetCADTH.set_column('W:W', None, date)
    worksheetCADTH.set_column('X:X', None, date)
    worksheetCADTH.set_column('Y:Y', None, date)

    # CADTH - Scraps table
    soup = scrapBaseUrl(BASE_URL_CADTH + PATH_CADTH)
    table_cadth = soup.find("table", class_=TABLE_CLASS_CADTH)

    # PCPA - Scraps table
    soup = scrapBaseUrl(BASE_URL_PCPA + PATH_PCPA)
    table_pcpa = soup.find("table", id=TABLE_CLASS_PCPA)

    # CADTH - Builds and writes excel's head
    excel_head = getExcelHead(table_cadth, THEAD_PRODUCT_CADTH)
    worksheetCADTH.write_row(0, 0, excel_head, bold)

    # PCPA - Builds and writes excel's head
    excel_head = getExcelHead(table_pcpa, THEAD_PRODUCT_PCPA)
    worksheetPCPA.write_row(0, 0, excel_head, bold)

    trs = table_cadth.find_all("tr")
    FILE_LINES = len(trs)
    NUM_WORKERS = cpu_count() * 2
    chunksize = FILE_LINES // NUM_WORKERS * 4   # Try to get a good chunksize. You're probably going to have to tweak this, though. Try smaller and lower values and see how performance changes.
    pool = Pool(NUM_WORKERS)

    row = 1
    result_iter = pool.imap(getExcelRow, trs)
    for result in result_iter:  # lazily iterate over results.
        print(result[0])
        worksheetCADTH.write_row(row, 0, result)
        row += 1
        print(row)
    
    # Close csv file
    workbook.close()

if __name__ == "__main__":
    run()