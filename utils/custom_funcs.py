import utils.funcs as f
from datetime import datetime

OUTPUT_FILE = "CADTH-pCPA-data-import.xlsx"
OUTPUT_FILE_TMP = "CADTH-pCPA-data-import-tmp.xlsx"
BASE_URL_CADTH = "https://www.cadth.ca"
PATH_CADTH = "/reimbursement-review-reports"
TABLE_CLASS_CADTH = "reimbursement_review"
TABLE_PRODUCT_CLASS_CADTH = "pcodr_table"
THEAD_PRODUCT_CADTH = ["Strength","Tumour Type","Funding Request","Pre Noc Submission","NOC Date","Manufacturer","Sponsor","Submission Date (Target Date)","Final CDR review report(s) posted","Submission Deemed Complete","Submission Type","Prioritization Requested","Stakeholder Input Deadline","Check-point meeting","pERC Meeting","Initial Recommendation Issued","Feedback Deadline","pERC Reconsideration Meeting","Notification to Implement Issued","Clarification"]

BASE_URL_PCPA = "https://www.pcpacanada.ca"
PATH_PCPA = "/negotiations"
TABLE_CLASS_PCPA = "datatable"
THEAD_PRODUCT_PCPA = ["pCPA File Number","Sponsor/Manufacturer","CADTH Project Number","pCPA Engagement Letter Issued","Negotiation Process Concluded"]

def dateParser_cadth(str):
    if str and str != 'N/A':
        return datetime.strptime(str, '%B %d, %Y')
    return str

def dateParser_pcpa(str):
    if str and str != 'Not Applicable':
        return datetime.strptime(str, '%Y-%m-%d')
    return str

# CADTH - Parse product table
def parseProductTable(element, product_tr_list):
    if product_tr_list.find("th", text=lambda t: t and element in t):
        product_td = product_tr_list.find("th", text=lambda t: t and element in t).find_next_sibling("td").get_text(separator=" ").strip()
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
def getProductDetail_cadth(soup):
    product_row = []

    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    #2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
    if soup.find("table", class_=TABLE_PRODUCT_CLASS_CADTH):
        product_tr_list = soup.find("table", class_=TABLE_PRODUCT_CLASS_CADTH)
        product_row = [parseProductTable(element, product_tr_list) for element in THEAD_PRODUCT_CADTH]

    #3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)
    #4th detected format (ex: https://www.cadth.ca/pegfilgrastim-6)
    elif soup.find("div", class_="publish-date"):
        product_row = [cleanProductElement(element, soup) for element in THEAD_PRODUCT_CADTH]

    else:
        product_row.append("Unable to fetch data, new web format")

    return product_row

# CADTH - Returns excel row as a string
def getExcelRow_cadth(tr):
    table_row = [e.get_text(separator=" ").strip() for e in tr.find_all("td")]

    # product url
    url_product = BASE_URL_CADTH + tr.td.a['href']
    table_row[0] = '=HYPERLINK("'+url_product+'", "'+table_row[0]+'")'

    soup = f.scrapBaseUrl(url_product)
    product_row = getProductDetail_cadth(soup)

    excel_row = table_row + product_row

    # Parse dates
    excel_row[5] = dateParser_cadth(excel_row[5])
    excel_row[6] = dateParser_cadth(excel_row[6])
    excel_row[12] = dateParser_cadth(excel_row[12])
    excel_row[15] = dateParser_cadth(excel_row[15])
    excel_row[16] = dateParser_cadth(excel_row[16])
    excel_row[17] = dateParser_cadth(excel_row[17])
    excel_row[20] = dateParser_cadth(excel_row[20])
    excel_row[21] = dateParser_cadth(excel_row[21])
    excel_row[22] = dateParser_cadth(excel_row[22])
    excel_row[23] = dateParser_cadth(excel_row[23])
    excel_row[24] = dateParser_cadth(excel_row[24])
    excel_row[25] = dateParser_cadth(excel_row[25])
    excel_row[26] = dateParser_cadth(excel_row[26])

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