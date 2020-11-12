#!/usr/bin/env python
import xlsxwriter
import xlwings as xw
import utils.funcs as f
import utils.custom_funcs as cf
import cProfile

workbook = None
app = None

def run_scraper():

    print('Scraping website... START')

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

    # Close csv file
    wb.close()

    print('Scraping website... END')

def override_sheet(name, range):
    global workbook

    print('Copying data to excel file... START')

    sNamList = [sh.name for sh in workbook.sheets]
    if name not in sNamList:
        workbook.sheets.add(name)

    source_wb = xw.books.open(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))
    source_wb.sheets[name].range(range).copy(workbook.sheets[name].range(range))
    workbook.save()
    source_wb.close()

    print('Copying data to excel file... END')

def run_from_exe():
    global workbook

    print('Running mode: run_from_exe')

    # Start process
    run_scraper()

    # Initialize Excel instance
    app = xw.App(visible=False)

    # Open or create a workbook
    try:
        workbook = app.books.open(f.getAbsolutePath(cf.OUTPUT_FILE))
    except:
        workbook_create = xlsxwriter.Workbook(f.getAbsolutePath(cf.OUTPUT_FILE), {'constant_memory': True})
        workbook_create.add_worksheet('CADTH')
        workbook_create.add_worksheet('pCPA')
        workbook_create.close()
        workbook = app.books.open(f.getAbsolutePath(cf.OUTPUT_FILE))

    override_sheet('CADTH', 'A1:AZ5000')
    override_sheet('pCPA', 'A1:AZ5000')

    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    workbook.close()
    app.quit()

    print('Scraper executed successfully! END')

def run_from_xlsb():
    global workbook

    print('Running mode: run_from_xlsb... START')

    # Current workbook and sheets
    workbook = xw.Book.caller()
    
    run_scraper()

    override_sheet('CADTH', 'A1:AZ5000')
    override_sheet('pCPA', 'A1:AZ5000')
    # Remove tmp file
    f.os.remove(f.getAbsolutePath(cf.OUTPUT_FILE_TMP))

    print('Scraper executed successfully! END')

if __name__ == "__main__":
    run_from_exe()