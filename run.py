from config import *
from functions import *

soup = scrapBaseUrl(BASE_URL_1 + PATH_1)

table = soup.find("table", class_=TABLE_CLASS_1)
thead = [e.text for e in table.find("thead").find_all("th")]
trs = table.find_all("tr")

#opens csv file
f = open('csvfile.csv','w')

#builds excel head
excel_head = SEPARATOR.join(thead) + '|url' + THEAD_PRODUCT_1 + '\n'

#builds excel data
#excel_data = ''
excel_row = ''
for tr in trs:
    
    excel_row = SEPARATOR.join( [e.text for e in tr.find_all("td")] )
    
    url_product = BASE_URL_1 + '' + tr.td.a['href']
    
    soup_product = scrapBaseUrl(url_product)

    row = ''
    #1st detected format (ex: https://www.cadth.ca/xalkori-resubmission-first-line-advanced-nsclc-details)
    if soup_product.find("table", class_=TABLE_PRODUCT_CLASS_1):
        product_table = soup_product.find("table", class_=TABLE_PRODUCT_CLASS_1)
        
        remove_list = ["Brand Name","Generic Name","Indication","Review Status","Final Recommendation Issued","Submission Date"]

        product_row = []
        for product_tr in product_table.find_all("tr"):
            if product_tr.find("th").text in remove_list:
                product_row.append("")
            else:
                product_row.append(product_tr.find("td").text)

        row = SEPARATOR.join(product_row)

    #2nd detected format (ex: https://www.cadth.ca/aripiprazole-25)    
    elif soup_product.find("div", class_="publish-date"):
        project_number = soup_product.find("div", class_="publish-project-number").find("span").text
        strength = ""
        tumour_type = ""
        funding_request = ""
        pre_noc_submission = ""
        noc_date = ""
        
        #clean manufacturer value
        manufacturer_name = soup_product.find("p", class_="field_manufacturer")
        manufacturer_name.strong.decompose()
        manufacturer_name = manufacturer_name.text
        
        sponsor = ""
        submission_deemed_completed = ""
        
        #clean submission type value value
        submission_type = soup_product.find("p", class_="field_submission_type")
        submission_type.strong.decompose()
        submission_type = submission_type.text
        
        prioritization_request = ""
        stakeholder_input_deadline = ""
        checkpoint_meeting = ""
        perc_meeting = ""
        initial_recommendation_issued = ""
        feedback_deadline = ""
        perc_reconsideration = ""
        notification_to_implement = ""
        clarification = ""

        row = project_number + '|' + strength + '|' + tumour_type + '|' + funding_request + '|' + pre_noc_submission + '|' + noc_date + '|' + manufacturer_name + '|' + sponsor + '|' + submission_deemed_completed + '|' + submission_type + '|' + prioritization_request + '|' + stakeholder_input_deadline + '|' + checkpoint_meeting + '|' + perc_meeting + '|' + initial_recommendation_issued + '|' + feedback_deadline + '|' + perc_reconsideration + '|' + notification_to_implement + '|' + clarification

    else:
        row = "Unable to fetch data, new web format"

    excel_row = excel_row + '|' + url_product + '|' + row + '\n'

    #print("ROW : " + excel_row + '\n')
    
#excel_data = excel_data + excel_row

f = open('csvfile.csv','w')
f.write(excel_head)
f.write(excel_row)
f.close()

#csvOpen = open('filename','w')
#c = csv.writer(csvOpen, dialect='excel')
#c.writerows(excel_data)

#f.write(th.string)
#f.write(th.string'hi there\n') # Python will convert \n to os.linesep

#for tr in trs:
    #for td in tr:
        #print(td.string)

#f.close()