from func import *

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

    # CADTH - Builds and writes excel's data
    row = 1
    for tr in table_cadth.find_all("tr"):
        excel_row = getExcelRow(tr)

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

        worksheetCADTH.write_row(row, 0, excel_row)
        row += 1
        if row == 10:
            break

    # Close csv file
    workbook.close()

run()