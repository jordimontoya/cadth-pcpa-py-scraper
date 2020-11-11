# catdh-pcpa-py-scraper

## Before execution
> Very important: Close entirely excel file "CADTH-pCPA-data-import.xlsx"! Otherwise the app will be unable to open the file.

## What you need to know
- Expected execution time: 1:30 - 2 minutes.
- Output excel file will be created next to `scraper.exe`
- Output excel file will be always called "CADTH-pCPA-data-import.xlsx"
- If file "CADTH-pCPA-data-import.xlsx" already exists, worksheets "CADTH" and "pCPA" will be overriden. Formulas, datatables and Pivot tables in other sheets inside this workbook will continue working after scraper execution.
- If "CADTH-pCPA-data-import.xlsx" file does not exists, workbook and worksheets "CADTH" and "pCPA" will be created from scratch.

## Guidelines
1. Close excel file "CADTH-pCPA-data-import.xlsx"
1. Double click on `scraper.exe`
2. A cmd command will pop. Wait and do nothing until it disapears.
3. Once cmd command closed, excel file "CADTH-pCPA-data-import.xlsx" ready to be used. Double check last modification datetime of the excel file.
