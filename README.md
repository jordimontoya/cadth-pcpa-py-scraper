# catdh-pcpa-py-scraper

By: [Codekubik](http://www.codekubik.com)

## Introduction
This python script pulls data from 2 different websites and creates/overrides an 2 Excel worksheets with the results.
`scraper.exe` will do the job.
Datasources are:
    - The *CADTH* sheet contains the data extracted from the [Canadian Reimbursement Review Reports datatable](https://www.cadth.ca/reimbursement-review-reports) among all product details for each record.
    - The *pCPA* sheet contains the data extracted from the [Pan-Canadian Pharmaceutical alliance](https://www.pcpacanada.ca/negotiations) among all product details for each record.


## What you need to know

- Expected execution time: between 1:30 - 2 minutes.
- Output excel file will be created next to `scraper.exe`
- Output excel file will be always called *CADTH-pCPA-data-import.xlsx*
- If file *CADTH-pCPA-data-import.xlsx* already exists, worksheets *CADTH* and *pCPA* will be overriden. Formulas, datatables and Pivot tables in other sheets inside this workbook will continue working after scraper execution.
- If *CADTH-pCPA-data-import.xlsx* file does not exists, workbook and worksheets *CADTH* and *pCPA* will be created from scratch.


## Guidelines
> **Very important:** Before every execution, close entirely excel file *CADTH-pCPA-data-import.xlsx*. Otherwise the app will be unable to open the file.

> Killing the execution before it ends may cause the excel file still open on the background. Just kill Excel process on Task Manager

#### Execute scraper.exe

1. Download executable file by clicking on `scraper.exe` and then `Download` button
2. If this is the first execution, right click and scan `scraper.exe` with your antivirus. Executable files coming from Internet are intercepted by all antivirus.
3. Double click on `scraper.exe`
4. A cmd command will pop. Wait and do nothing until it disapears.
5. Once cmd command closed, excel *CADTH-pCPA-data-import.xlsx* is ready to be used. Double check excel's last modification datetime.

#### Execute from IDE or Command line (only for development purposes)

1. Download and install [Python 3.9](https://www.python.org/downloads/release/python-390/) and `PIP`
2. Add python to system env variables
3. Download code source `cadth-pcpa-py-scraper`
4. Open cmd and execute pip install to import below libraries:
    - `pip install xlsxwriter`
    - `pip install xlwings`
    - `pip install beautifulsoup4`
    - `pip install multiprocess`
    - `pip install DateTime`
5. Open cmd --> go to python directory --> execute command `python scraper.py`
6. Once script execution ends, excel file *CADTH-pCPA-data-import.xlsx* is ready to be used. Double check excel's last modification datetime.
