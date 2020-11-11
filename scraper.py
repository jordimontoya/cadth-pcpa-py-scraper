import xlsxwriter
import xlwings as xw
import utils.funcs as f
import utils.custom_funcs as cf
import cProfile

workbook = None
app = None

def run_scraper():
    # Create a workbook and declare specific formats.
    wb = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE_TMP), {'constant_memory': True})
    bold = wb.add_format({'bold': True})
    underline = wb.get_default_url_format()
    date = wb.add_format({'num_format': 'dd-mmm-yyyy'})

    # PCPA - Create worksheet and set link format and date format
    worksheetPCPA = wb.add_worksheet('pCPA')
    worksheetPCPA.set_column('A:A', None, underline)
    worksheetPCPA.set_column('H:H', None, date)
    worksheetPCPA.set_column('I:I', None, date)

    # PCPA - Scraps table
    soup = f.scrapBaseUrl(cf.BASE_URL_PCPA + cf.PATH_PCPA)
    table_pcpa = soup.find("table", id=cf.TABLE_CLASS_PCPA)

    # PCPA - Builds and writes excel's head
    excel_head = f.getExcelHead(table_pcpa, cf.THEAD_PRODUCT_PCPA)
    worksheetPCPA.write_row(0, 0, excel_head, bold)

    # PCPA - Builds and writes data to excel
    trs = table_pcpa.find('tbody').find_all("tr")
    #trs = trs[:10]
    f.excel_writer(cf.getExcelRow_pcpa, worksheetPCPA, trs)
    
    # CADTH - Create worksheet and set link format and date format
    worksheetCADTH = wb.add_worksheet('CADTH')
    worksheetCADTH.set_column('A:A', None, underline)
    worksheetCADTH.set_column('F:F', None, date)
    worksheetCADTH.set_column('G:G', None, date)
    worksheetCADTH.set_column('M:M', None, date)
    worksheetCADTH.set_column('P:P', None, date)
    worksheetCADTH.set_column('Q:Q', None, date)
    worksheetCADTH.set_column('R:R', None, date)
    worksheetCADTH.set_column('U:U', None, date)
    worksheetCADTH.set_column('V:V', None, date)
    worksheetCADTH.set_column('W:W', None, date)
    worksheetCADTH.set_column('X:X', None, date)
    worksheetCADTH.set_column('Y:Y', None, date)
    worksheetCADTH.set_column('Z:Z', None, date)
    worksheetCADTH.set_column('AA:AA', None, date)

    # CADTH - Scraps table
    soup = f.scrapBaseUrl(cf.BASE_URL_CADTH + cf.PATH_CADTH)
    table_cadth = soup.find("table", class_=cf.TABLE_CLASS_CADTH)

    # CADTH - Builds and writes excel's head
    excel_head = f.getExcelHead(table_cadth, cf.THEAD_PRODUCT_CADTH)
    worksheetCADTH.write_row(0, 0, excel_head, bold)

    # CADTH - Builds and writes data to excel
    trs = table_cadth.find_all("tr")
    #trs = trs[:10]
    f.excel_writer(cf.getExcelRow_cadth, worksheetCADTH, trs)
    print(wb.sheetnames)
    # Close csv file
    wb.close()

def override_excel():
    global workbook

    # File and sheets to copy
    source_wb = xw.books.open(r''+f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    # Copy needed source_sheets to the current sheets
    f.deleteSheet(workbook, 'CADTH')
    f.deleteSheet(workbook, 'pCPA')
    
    workbook.sheets.add("Temp", after=1)

    source_wb.sheets['CADTH'].api.Copy(Before=workbook.sheets['Temp'].api)
    source_wb.sheets['pCPA'].api.Copy(Before=workbook.sheets['Temp'].api)

    workbook.save()

    f.deleteSheet(workbook, 'Temp')
    workbook.save()
    
    source_wb.close()

    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

def run_from_exe():
    global workbook
    
    # Initialize Excel instance
    app = xw.App(visible=False)

    # Open or create a workbook
    try:
        workbook = app.books.open(f.getAbsolutePath(cf.OUTPUT_FILE))
    except:
        workbook_create = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE), {'constant_memory': True})
        workbook_create.add_worksheet('sheet1')
        workbook_create.add_worksheet('CADTH')
        workbook_create.add_worksheet('pCPA')
        workbook_create.close()
        workbook = app.books.open(r''+f.getAbsolutePath(cf.OUTPUT_FILE))

    # Start process
    run_scraper()
    override_excel()

    workbook.close()
    app.quit()

def run_from_xlsb():
    global workbook

    # Current workbook and sheets
    workbook = xw.Book.caller()

    # Start process
    run_scraper()
    override_excel()

if __name__ == "__main__":
    run_from_exe()