# sphinx-l10n
Fan translation scripts and mod content for Sphinx and the Cursed Mummy.

> Like most people, if you only need to translate you can skip all this and help by joining the
> Transifex project and then edit your translation from the web interface. That's it:
> https://app.transifex.com/swyter/sphinx-l10n

# Install the *Unofficial Language Pack* from the *Workshop*
If you just want to play in one of the supported community languages, follow the steps below:
1. Join [here](https://steamcommunity.com/groups/satcm) first while logged-in to see the beta *Steam Workshop* page.
   * Without this you will get an error in the second step.
2. Click on the green *Subscribe* button [here](https://steamcommunity.com/sharedfiles/filedetails/?id=3138744735) and make sure the base game is installed.
   * Steam will download the mod automatically.
3. Copy and paste the launch arguments shown in the [Workshop entry description](https://steamcommunity.com/sharedfiles/filedetails/?id=3138744735#highlightContent) to enable the mod.
4. Launch the game from your Steam Library, and play.
   * Remove the launch arguments if you want to play the normal game or any other mod.

# How to use

* Most of the original game text is originally stored in an Excel file called `SphinxText.xls` that you can find under the `_mod/Sphinx/Grafix/Spreadsheets` folder here.
   * This originally comes from the [_Authoring Tools_](https://sphinxandthecursedmummy.fandom.com/wiki/Authoring_Tools) DLC.
* Everything is laid out in a single spreadsheet, with each language having its own column.
* To make the game easier to fan-translate we are using a nifty web tool called Transifex.
* Because Sphinx uses an exotic format we need to convert it to something that Transifex understands.
* It works more or less like this:

```
┌───────────────────────┐  ┌─────┐                            ┌──────────────────────────────────────┐
│SphinxText.xls         │->│.CSV │-> sphinx-l10n-export.py -> │ JSON files compatible with Transifex │
└───────────────────────┘  └─────┘                            └──────────────────────────────────────┘
┌───────────────────────┐  ┌─────┐                            /      V                   Λ
│SphinxTextImported.xls │<-│.CSV │<- sphinx-l10n-import.py <-´       |                   |
└───────────────────────┘  └─────┘                                  PUSH ┌───────────┐ PULL
                                                                      \__│ TRANSIFEX │__/
                                                                         └───────────┘
                                                                      (with tx.cmd/tx.sh)
```


* On Linux, you would need to install the [Transifex Client](https://docs.transifex.com/client/installing-the-client) and Python. This is already bundled for Windows.
* Optionally, Gnumeric comes with a handy `ssconvert` tool, useful to turn CSV files into XLS (and vice versa) in a jiffy, without having to use LibreOffice or Excel. Also included for Windows.
* For Linux users it all boils down to opening your terminal and using something like this:
```
tx.sh && python sphinx-l10n-import.py && ssconvert SphinxTextImported.csv SphinxTextImported.xls
```

>  1. `tx.sh` pulls the latest changes from Transifex and updates the JSON files.
>  2. `sphinx-l10n-import.py` turns the local language JSON files into a single CSV file for all
>      the languages, by using the local `SphinxText.csv` as template.
>  3. `ssconvert` turns the CSV into a ready-to-use replacement of `SphinxText.xls`. Called `SphinxTextImported.xls`.


 # Making a mod on Windows + pulling from Transifex

Get your text into `SphinxText.xls` either via the Transifex scripts or just typing in *Excel* or *LibreOffice* (free). Open `TextMod.elf` with *Euroland Redux* and output (export) the PC version of `Text.edb`, the game will read it and you can ship the `_mod` folder as a standalone mod. To see how it works from the game side, see the [*Localization*](https://sphinxandthecursedmummy.wikia.com/wiki/Localization) wiki page.

In more detail, here are the steps:
1. Make a Transifex account to translate the project via the web interface.
2. Run `tx.cmd` to automatically download/pull the latest translation progress from the site and write it into `SphinxText.xls`.
   * The first time around it will ask you for a secret code that you need to generate from [here](https://www.transifex.com/user/settings/api/), paste it into the window by right-clicking once and then press *Enter*. The code looks like this: `1/1290349033429802359034903402339040767759`.
1. Double-click to run `mount-virtual-x-drive.bat` from the `_mod` folder.
   * Now you should have a new `X:` drive in *My PC* with the same files you see under `_mod`; they are mirrored.
   * You will only need to do this once, when the drive is missing.
2. Enable and install the *Authoring Tools* DLC included with Sphinx and open your local game folder, the DLC is stored under `Tools`. Go to `Tools/EngineX/utils` and launch `EuroLandRedux.exe`; the all-in-one editor.
   * This will only work if the `X:` drive is around.
   * Also, keep in mind that the original EuroLand (`EuroLand.exe`) won't export spreadsheets correctly.
3. Open `X:\Sphinx\Grafix\Maps\Misc\TextMod.ELF` with _EuroLand Redux_. Via the _File > Open_ menu.
4. In the ELF tree, expand *App Targets*, right-click on _PC_ and click on _Output (Optimised)_.
   * If everything goes well you should see a new, exported `Text.edb` file appear in the `X:\Sphinx\Binary\_bin_PC` folder. That's what the game will ultimately read.
   * ELF stands for *EuroLand File*, and EDB is the final generated *EngineX DB* format.
6. Launch the game with the `launch-sphinx-mod-dev.cmd` script under the `_mod` folder.
   * It will automatically find the game and call it with the `-dev -lang system -mod <_mod-path>` arguments.

If you need help, we have a `#translations` channel in the [official Sphinx Discord](https://discord.gg/sphinx) server.
