import xlsxwriter
import xlwings as xw
import funcs as f
import custom_funcs as cf
import cProfile

workbook = None
app = None

def run_scraper():
    # Create a workbook and declare specific formats.
    wb = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE), {'constant_memory': True})
    bold = wb.add_format({'bold': True})
    underline = wb.get_default_url_format()
    date = wb.add_format({'num_format': 'dd-mmm-yyyy'})

    # PCPA - Create worksheet and set link format and date format
    worksheetPCPA = wb.add_worksheet('pCPA')
    worksheetPCPA.set_column('A:A', None, underline)
    worksheetPCPA.set_column('I:I', None, date)
    worksheetPCPA.set_column('J:J', None, date)

    # PCPA - Scraps table
    soup = f.scrapBaseUrl(cf.BASE_URL_PCPA + cf.PATH_PCPA)
    table_pcpa = soup.find("table", id=cf.TABLE_CLASS_PCPA)

    # PCPA - Builds and writes excel's head
    excel_head = f.getExcelHead(table_pcpa, cf.THEAD_PRODUCT_PCPA)
    worksheetPCPA.write_row(0, 0, excel_head, bold)

    # PCPA - Builds and writes data to excel
    trs = table_pcpa.find('tbody').find_all("tr")
    #trs = trs[:30]
    f.excel_writer(cf.getExcelRow_pcpa, worksheetPCPA, trs)
    
    # CADTH - Create worksheet and set link format and date format
    worksheetCADTH = wb.add_worksheet('CADTH')
    worksheetCADTH.set_column('A:A', None, underline)
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
    soup = f.scrapBaseUrl(cf.BASE_URL_CADTH + cf.PATH_CADTH)
    table_cadth = soup.find("table", class_=cf.TABLE_CLASS_CADTH)

    # CADTH - Builds and writes excel's head
    excel_head = f.getExcelHead(table_cadth, cf.THEAD_PRODUCT_CADTH)
    worksheetCADTH.write_row(0, 0, excel_head, bold)

    # CADTH - Builds and writes data to excel
    trs = table_cadth.find_all("tr")
    #trs = trs[:30]
    f.excel_writer(cf.getExcelRow_cadth, worksheetCADTH, trs)

    # Close csv file
    wb.close()

def run():
    run_scraper()

    # file and sheets to copy
    source_wb = xw.books.open(r''+cf.OUTPUT_FILE)

    # copy needed source_sheets to the current sheets
    f.deleteSheet(workbook, 'CADTH')
    f.deleteSheet(workbook, 'pCPA')

    sht1 = source_wb.sheets["CADTH"]
    sht2 = source_wb.sheets["pCPA"]
    print(source_wb.sheets)
    
    workbook.sheets.add("Temp", after=1)
    print(workbook.sheets)
    sht1.api.Copy(Before=workbook.sheets['Temp'].api)

    #source_wb.sheets['CADTH'].api.Copy(Before=workbook.sheets[1].api)
    #source_wb.sheets['pCPA'].api.Copy(Before=workbook.sheets[1].api)
    
    

    source_wb.close()
    workbook.save()
    #os.remove(getAbsolutePath(OUTPUT_FILE_TMP))

def run_from_exe():
    global workbook
    # Open or create a workbook.
    
    #app = xw.App(visible=True)

    #try:
        #workbook = app.books(getAbsolutePath(OUTPUT_FILE))
    #except:
        #print("gola")
        #workbook_create = xlsxwriter.Workbook(r''+getAbsolutePath(OUTPUT_FILE), {'constant_memory': True})
        #workbook_create.add_worksheet('sheet1')
        #workbook_create.add_worksheet('CADTH')
        #workbook_create.add_worksheet('pCPA')
        #workbook_create.close()
        #workbook = app.books(r''+getAbsolutePath(OUTPUT_FILE))
    #workbook.save()
    run_scraper()

    #workbook.close()
    #app.quit()

def run_from_xlsb():
    global workbook

    # Current workbook and sheets
    workbook = xw.Book.caller()
    run()

if __name__ == "__main__":
    run_from_exe()