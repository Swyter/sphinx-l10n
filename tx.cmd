MODE CON: COLS=110
@echo off && title Updating translations from Transifex...
:up

::push our latest strings to the web
::tx push -s -t -f --skip --no-interactive
::tx push -s -f --skip --no-interactive
::tx push -s -t -f --skip --no-interactive
::tx push -t -l sv --skip --no-interactive
::tx push -t -l zh-Hant --skip --no-interactive
::tx push -s -t -l en,en_GB,es,fr,it --skip --no-interactive
::tx push -s -r sphinx-l10n.main_inv_description --skip

::pull latest translations
tx pull -a -f --skip --minimum-perc=3 --workers 20 --silent

echo. 
echo --
echo [i] Pulled from Transifex! Press any key to run the Transifex JSON
echo     to CSV conversion script and then turn that into Excel.
echo. 
echo     Note: This will overwrite your local SphinxText.xls progress! && pause
echo. 
:: https://www.python.org/ftp/python/3.11.5/python-3.11.5-embed-win32.zip
.tx\python\python sphinx-l10n-import.py

echo. 
echo --
echo [i] Converted from Transifex JSON folders to SphinxTextImported.csv
echo     Now converting the CSV into SphinxText.xls
:: https://download.cnet.com/Gnumeric/3001-2077_4-10968476.html (1.10.16) extracted via 7-zip
.tx\gnumeric\bin\ssconvert.exe --import-encoding=utf8 SphinxTextImported.csv _mod/Sphinx/Grafix/Spreadsheets/SphinxText.xls 2>nul

echo --
echo Done! You can either close the window or press Enter again to restart the whole thing && pause
echo. 
cls && goto :up