import utils.funcs as f
from datetime import datetime

OUTPUT_FILE = "CADTH-pCPA-data-import.xlsx"
OUTPUT_FILE_TMP = "CADTH-pCPA-data-import-tmp.xlsx"
BASE_URL_CADTH = "https://www.cadth.ca"
PATH_CADTH = "/reimbursement-review-reports?search_api_fulltext=&field_project_type=All&items_per_page=50&page={}"
TABLE_CLASS_CADTH = "views-view-table"
THEAD_PRODUCT_CADTH = ["Project Number","Project Line","Strength","Tumour Type","Funding Request","Pre Noc Submission","NOC Date","Manufacturer","Sponsor","Submission Date (Target Date)","Final CDR review report(s) posted","Submission Deemed Complete","Submission Type","Prioritization Requested","Stakeholder Input Deadline","Check-point meeting","pERC Meeting","Initial Recommendation Issued","Feedback Deadline","pERC Reconsideration Meeting","Notification to Implement Issued","Clarification"]

BASE_URL_PCPA = "https://www.pcpacanada.ca"
PATH_PCPA = "/negotiations"
TABLE_CLASS_PCPA = "datatable"
THEAD_PRODUCT_PCPA = ["pCPA File Number","Sponsor/Manufacturer","CADTH Project Number","pCPA Engagement Letter Issued","Negotiation Process Concluded"]

def dateParserShort_cadth(str):
    if str and str != 'N/A' and 'Requested' not in str:
        return datetime.strptime(str, '%b %d, %Y')
    return str

def dateParser_cadth(str):
    if str and str != 'N/A' and 'Requested' not in str:
        return datetime.strptime(str, '%B %d, %Y')
    return str

def dateParser_pcpa(str):
    if str and str != 'Not Applicable':
        return datetime.strptime(str, '%Y-%m-%d')
    return str

# CADTH - Parse product table
def parseProductTable(element, product_content):
    if product_content.find("strong", text=lambda t: t and element in t):
        product_td = product_content.find("strong", text=lambda t: t and element in t)
        product_td = product_td.parent
        product_td = product_td.find_next_sibling("div").get_text(separator=" ").strip()
        product_td = product_td.replace('\n', ' ').replace('\r', '')
        return product_td

    return ""

# CADTH - Clean product element detail
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

    elif soup.find("table", class_="cdr_milestones_table"):
        product_tr_list = soup.find("table", class_="cdr_milestones_table")
        if product_tr_list.find("th", text=lambda t: t and element in t):
            product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
            product_td = product_td.replace('\n', ' ').replace('\r', '')
            return product_td
        
    return ""

# CADTH - Clean product element detail
def replaceEmptyProductElement(product_row, element, product_tr_list):
    if product_tr_list.find("th", text=lambda t: t and element in t):
        product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
        product_td = product_td.replace('\n', ' ').replace('\r', '')
        return product_td

    return product_row

# CADTH - Returns the detail row as a string
#1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
#2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
#3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)
#4th detected format (ex: https://www.cadth.ca/pegfilgrastim-6)
def getProductDetail_cadth(soup):
    product_row = []

    if soup.find("div", class_="grid__col--md-9 page__content"):
        product_content = soup.find("div", class_="grid__col--md-9 page__content")
        product_row = [parseProductTable(element, product_content) for element in THEAD_PRODUCT_CADTH]
    else:
        product_row.append("Unable to fetch data")
        
    return product_row

# CADTH - Returns excel row as a string
def getExcelRow_cadth(tr):
    table_row = [e.get_text(separator=" ").strip() for e in tr.find_all("td")]

    # product url
    url_product = BASE_URL_CADTH + tr.td.a['href']
    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = f.scrapBaseUrl(url_product)
    product_row = getProductDetail_cadth(soup)

    if url_product:
        excel_row = table_row + product_row

    # Parse dates
    excel_row[5] = dateParserShort_cadth(excel_row[5])
    excel_row[6] = dateParserShort_cadth(excel_row[6])
    excel_row[13] = dateParser_cadth(excel_row[13])
    excel_row[16] = dateParser_cadth(excel_row[16])
    excel_row[18] = dateParser_cadth(excel_row[18])
    excel_row[21] = dateParser_cadth(excel_row[21])
    excel_row[22] = dateParser_cadth(excel_row[22])
    excel_row[23] = dateParser_cadth(excel_row[23])
    excel_row[24] = dateParser_cadth(excel_row[24])
    excel_row[25] = dateParser_cadth(excel_row[25])
    excel_row[26] = dateParser_cadth(excel_row[26])
    excel_row[27] = dateParser_cadth(excel_row[27])

    return excel_row

# CADTH - Returns the detail row as a string
def getProductDetail_pcpa(soup):
    product_row = []
    product_row.append(soup.find("span", class_="views-label-nid").find_next_sibling("span").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-manufacturer-name").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-cadth-project-id").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-engagement-date").find_next_sibling("div").get_text(separator=" ").strip())
    product_row.append(soup.find("span", class_="views-label-field-close-date").find_next_sibling("div").get_text(separator=" ").strip())
    
    return product_row

# CADTH - Returns excel row as a string
def getExcelRow_pcpa(tr):
    table_row = [e.get_text(separator=" ").strip() for e in tr.find_all("td")]

    # product url
    url_product = BASE_URL_PCPA + tr.td.a['href']
    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = f.scrapBaseUrl(url_product)
    product_row = getProductDetail_pcpa(soup)

    excel_row = table_row + product_row

    # Parse dates
    excel_row[7] = dateParser_pcpa(excel_row[7])
    excel_row[8] = dateParser_pcpa(excel_row[8])

    return excel_row