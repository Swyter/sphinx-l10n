# sphinx-l10n
Fan translation scripts and mod content for Sphinx and the Cursed Mummy.

> Like most people, if you only need to translate you can skip all this and help by joining the
> Transifex project and then edit your translation from the web interface. That's it:
> http://transifex.com/projects/p/sphinx-l10n


# How to use

* Most of the original game text is originally stored in an Excel file called `SphinxText.xls` that you can find under the `Tools/Sphinx/Grafix/Spreadsheets` folder of in the [_Authoring Tools_](https://sphinxandthecursedmummy.fandom.com/wiki/Authoring_Tools) DLC.
* Everything is laid out in a single spreadsheet, with each language having its own column.
* To make the game easier to fan-translate we are using a nifty web tool called Transifex.
* Because Sphinx uses an exotic format we need to convert it to something that Transifex understands.
* It works more or less like this:

```
┌────────────────────────┐  ┌─────┐                            ┌──────────────────────────────────────┐ 
│ SphinxText.xls         │->│.CSV │-> sphinx-l10n-export.py -> │ JSON files compatible with Transifex │
└────────────────────────┘  └─────┘                            └──────────────────────────────────────┘
┌────────────────────────┐  ┌─────┐                            /      V                   Λ
│ SphinxTextImported.xls │<-│.CSV │<- sphinx-l10n-import.py <-´       |                   |
└────────────────────────┘  └─────┘                                  PUSH ┌───────────┐ PULL
                                                                       \__│ TRANSIFEX │__/
                                                                          └───────────┘ 
                                                                       (with tx.cmd/tx.sh)
```


* On Linux, you would need to install the [Transifex Client](https://docs.transifex.com/client/installing-the-client) and Python.
* Optionally, Gnumeric comes with a handy `ssconvert` tool, useful to turn CSV files into XLS (and vice versa) in a jiffy, without having to use LibreOffice or Excel.
* It all boils down to opening your terminal and using something like this:
```
tx.sh && python sphinx-l10n-import.py && ssconvert SphinxTextImported.csv SphinxTextImported.xls
```

>  1. `tx.sh` pulls the latest changes from Transifex and updates the JSON files.
>  2. `sphinx-l10n-import.py` turns the local language JSON files into a single CSV file for all
>      the languages, by using the local `SphinxText.csv` as template.
>  3. `ssconvert` turns the CSV into a ready-to-use replacement of `SphinxText.xls`. Called `SphinxTextImported.xls`.
  
  
 # Making a mod

Rename your file to `SphinxText.xls`, place it in `X:\Sphinx\Grafix\Spreadsheets\SphinxText.xls`, open `Text.elf` with Euroland Redux and output (export) the PC version of `Text.edb`, the game will read it and you can ship it as a mod.


If you need help, we have a `#translations` channel in the [official Sphinx Discord](https://discord.gg/sphinx) server.
