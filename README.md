# sphinx-l10n
Fan translation scripts and mod content for Sphinx and the Cursed Mummy.

You can help by joining the Transifex project and editing from the web interface:
http://transifex.com/projects/p/sphinx-l10n


# How to use

* Most of the original game text is originally stored in an Excel file called `SphinxText.xls` that you can find under the `Tools/Sphinx/Grafix/Spreadsheets` folder of in the [_Authoring Tools_](https://sphinxandthecursedmummy.fandom.com/wiki/Authoring_Tools) DLC.
* Everything is laid out in a single spreadsheet, with each language having its own column.
* To make the game easier to fan-translate we are using a nifty web tool Transifex.
* Because Sphinx uses an exotic format we need to convert it to something that Transifex understands.


```
┌────────────────────────┐    ┌─────┐
│ SphinxText.xls         │ => │.CSV │ => sphinx-l10n-export.py =>  ┌──────────────────────────────────────┐ 
└────────────────────────┘    └─────┘                              │ JSON files compatible with Transifex │
┌────────────────────────┐    ┌─────┐                              └──────────────────────────────────────┘
│ SphinxTextImported.xls │ <= │.CSV │ <= sphinx-l10n-import.py <=            V                   Λ
└────────────────────────┘    └─────┘                                        |                   |
                                                                            PUSH ┌───────────┐ PULL (with tx.cmd/tx.sh)
                                                                              \__│ TRANSIFEX │__/
                                                                                 └───────────┘ 
```
