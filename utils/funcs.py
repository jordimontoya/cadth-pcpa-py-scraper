import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from multiprocessing.dummy import Pool  # This is a thread-based Pool
from multiprocessing import cpu_count

def getAbsolutePath(relative_path):
    script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
    abs_path = os.path.join(script_dir, relative_path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    return os.path.abspath(abs_path)

def scrapBaseUrl(url):
    headers = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}
    r = requests.get(url, headers=headers)
    r.raw.chunked = True
    r.encoding = 'utf-8'
    return BeautifulSoup(r.text, 'lxml')

def dateParser_cadth(str):
    if str and str != 'N/A':
        return datetime.strptime(str, '%B %d, %Y')
    return str

def dateParser_pcpa(str):
    if str and str != 'Not Applicable':
        return datetime.strptime(str, '%Y-%m-%d')
    return str

def deleteSheet(wb, sheet_name):
    for sheet in wb.sheets:
        if sheet_name in sheet.name:
            sheet.delete()

# Returns excel columns' head as array
def getExcelHead(table, arr_head):
    thead = [e.text for e in table.find("thead").find_all("th")]
    return thead + arr_head

def excel_writer(func_name, worksheet, trs):   
    FILE_LINES = len(trs)
    NUM_WORKERS = cpu_count() * 2
    chunksize = FILE_LINES // NUM_WORKERS * 4
    pool = Pool(NUM_WORKERS)

    row = 1
    result_iter = pool.imap(func_name, trs)
    for result in result_iter:
        worksheet.write_row(row, 0, result)
        row += 1