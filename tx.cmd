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

echo Pulled from Transifex! Press any key to run
echo the import to CSV script and then turn that into XLS && pause

python sphinx-l10n-import.py
wsl.exe -- ssconvert SphinxTextImported.csv _mod/Sphinx/Grafix/Spreadsheets/SphinxText.xls

echo Done! && pause
cls && goto :up