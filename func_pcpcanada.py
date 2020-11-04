SEPARATOR = '|'
BASE_URL = "https://www.pcpacanada.ca"
PATH = "/negotiations"
OUTPUT_FILE = "output/pcpacanada.csv"
TABLE_CLASS = "reimbursement_review"
TABLE_PRODUCT_CLASS = "pcodr_table"
THEAD_PRODUCT = ["Strength","Tumour Type","Funding Request","Pre Noc Submission","NOC Date","Manufacturer","Sponsor","Submission Deemed Complete","Submission Type","Prioritization Requested","Stakeholder Input Deadline","Check-point meeting","pERC Meeting","Initial Recommendation Issued","Feedback Deadline","pERC Reconsideration Meeting","Notification to Implement Issued","Clarification"]

# Returns excel columns' head as a string
def getExcelHead(table, arr_head):
    thead = [e.text for e in table.find("thead").find_all("th")]
    return SEPARATOR.join(thead) + SEPARATOR + 'url' + SEPARATOR + SEPARATOR.join(arr_head) + '\n'

# Returns excel row as a string
def getExcelRow(tr):
    table_row = SEPARATOR.join( [e.get_text(separator=" ").strip() for e in tr.find_all("td")] )
    print(table_row + '\n')

    url_product = BASE_URL + '' + tr.td.a['href']
    soup = scrapBaseUrl(url_product)
    product_detail = getProductDetail(soup)

    return table_row + SEPARATOR + url_product + SEPARATOR + product_detail + '\n'

# Returns the detail row as a string
def getProductDetail(soup):
    row = ''

    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    #2nd detected format (ex: https://www.cadth.ca/ibrutinib-imbruvica-leukemia)
    if soup.find("table", class_=TABLE_PRODUCT_CLASS):

        product_tr_list = soup.find("table", class_=TABLE_PRODUCT_CLASS)
        product_row = []

        for element in THEAD_PRODUCT:
            if product_tr_list.find("th", string=element):
                product_td = product_tr_list.find("th", string=element).find_next_sibling("td").get_text(separator=" ").strip()
                product_td = product_td.replace('\n', ' ').replace('\r', '')
                product_row.append(product_td)
            else:
                product_row.append("")

        row = SEPARATOR.join(product_row)

    #3rd detected format (ex: https://www.cadth.ca/aripiprazole-25)    
    elif soup.find("div", class_="publish-date"):
        for element in THEAD_PRODUCT:
            
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

            row = row + SEPARATOR
    else:
        row = "Unable to fetch data, new web format"

    return row