import csv
import os
import json
import collections

HEADER_ROW       = 3 - 1 # swy: the header row is usually in the third line (2 when indexing from zero)
DEAD_TEXT_COLUMN = 3 - 1 # swy: this is hardcoded for the column in SphinxText.xls, edit accordingly

lang = {
    'MARKER_ENGLISH_US': 'en',
    'MARKER_ENGLISH_UK': 'en-GB',
    'MARKER_GERMAN':     'de',
    'MARKER_FRENCH':     'fr',
    'MARKER_SPANISH':    'es',
    'MARKER_ITALIAN':    'it',
    'MARKER_KOREAN':     'ko',
    'MARKER_JAPANESE':   'ja',
    'MARKER_BRAZILIAN':  'pt-BR',
    'MARKER_LATVIAN':    'lv',
    'MARKER_GREEK':      'el'
}

ignored_languages = [ 'ja' ]
ignored_section_markers = [ 'M_BOS_EFFECTS' ]
ignored_section_strings = [
    'HT_Text_Context_Blank', # '', 'TO DO', 'DOES NOT APPEAR IN INVENTORY', 'TEST'
    'HT_Text_Context_Test',
    'HT_Text_ES_E_BOSItem',
    'HT_Text_ES_E_BOSLocation',
    'HT_Text_ES_E_HelpText',
    'HT_Text_ES_S_BOSItem',
    'HT_Text_ES_S_BOSLocation',
    'HT_Text_ES_S_HelpText',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue01',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue02',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue03',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue04',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue05',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue06',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue07',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue08',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue09',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue10',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue11',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue12',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue13',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue14',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue15',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue16',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue17',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue18',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue19',
    'HT_Text_Hel_CursedPalace_FortuneTeller_AnkhPieceClue20',
    'HT_Text_Inv_Dsc_BronzeAnkh',
    'HT_Text_Inv_Dsc_DummyItem',
    'HT_Text_Inv_Dsc_FL04_Skeletal_Bat',
    'HT_Text_Inv_Dsc_FL04_Skeletal_Bat_Fire',
    'HT_Text_Inv_Dsc_FL06_Undead_Man',
    'HT_Text_Inv_Dsc_HD09_Horned_ReptileMan',
    'HT_Text_Inv_Dsc_HD13_S02_Aby_Bourgeoisie_Racist',
    'HT_Text_Inv_Dsc_HD15_GuardTest',
    'HT_Text_Inv_Dsc_KaDart',
    'HT_Text_Inv_Dsc_PI01_Green_Piranha',
    'HT_Text_Inv_Dsc_PI05_Aka_Turtle',
    'HT_Text_Inv_Dsc_PI06_Aka_Tentacle_Creature',
    'HT_Text_Inv_Dsc_PL01_Eye',
    'HT_Text_Inv_Dsc_PossessionDart',
    'HT_Text_Inv_DummyItem',
    'HT_Text_Memcard_Test'
]

data_read = []

# swy: parse the SphinxText.csv and load it as a row-major list
with open('SphinxText.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    data_read = [row for row in reader]

# swy: verify that it's the real thing; it can also be SHEET_TYPE_DATA
if (data_read[0][0] != "SHEET_TYPE_TEXT"):
    print("error: this needs to be a EuroLand text spreadsheet dump.")
    exit(-1)

# swy: programmatically find the correct header row index
for i, row in enumerate(data_read):
    if len(row) > 1 and row[0] == "MARKER_FORMAT_ROW":
        HEADER_ROW = i
        break

print("head", HEADER_ROW)

# swy: also get the correct column indexes for this spreadsheet from the header row
MARKER_HASHCODE_COLUMN       = data_read[HEADER_ROW].index("MARKER_HASHCODE")
MARKER_LANGUAGE_START_COLUMN = data_read[HEADER_ROW].index("MARKER_LANGUAGE_START")
MARKER_LANGUAGE_END_COLUMN   = data_read[HEADER_ROW].index("MARKER_LANGUAGE_END")

for cur in lang:
    # swy: check that this spreadsheet actually contains a column for this language, it can happen
    if (cur not in data_read[HEADER_ROW]):
        print("warning: doesn't seem like this spreadsheet contains a %s; skipping it..." % cur)
        continue
        
    # swy: some language columns are blank in the original translation; don't overwrite them
    if cur in ignored_languages:
        continue

    # swy: get the column index for the current language
    CUR_LANG_COLUMN = data_read[HEADER_ROW].index(cur)
    print(cur, lang[cur], "INDEX THING", CUR_LANG_COLUMN)

    # swy: create a folder with the language code if it's not already there
    if not os.path.exists(lang[cur]):
        os.mkdir(lang[cur])

    # swy: reset the section and output data; once per language in the loop
    cur_section = ""
    cur_section_count = 0
    out = collections.OrderedDict()

    # swy: iterate for all the rows, once per language
    for i, row in enumerate(data_read):
        # swy: skip empty rows
        if len(row) < 3:
            continue

        # swy: skip anything that goes before the actual table
        if i <= HEADER_ROW:
            continue

        # swy: skip empty cells
        if not row[0] and not row[MARKER_HASHCODE_COLUMN]:
            continue

        # swy: stop parsing once the table ends
        if row[0] == "MARKER_LAST_MESSAGE":
            break

        # swy: change string M_SOMETHING sections and spew the previous one if it wasn't empty
        if row[0] != "" and cur_section != row[0]:
            print(">> pre_section", cur_section)
            
            # swy: blank out ignored sections altogether :)
            if cur_section in ignored_section_markers:
                print(" [s] ignoring section %s" % row[0])
                out = collections.OrderedDict()

            if out: # swy: don't sort the files so that they appear in the correct section order, simplify the marker format instead
                with open("%s/%s.json" % (lang[cur], cur_section.replace("M_", "").lower()), 'w') as outfile:
                    json.dump(out, outfile, indent=2, ensure_ascii=False)

            cur_section_count = cur_section_count + 1
            cur_section = row[0];
            out = collections.OrderedDict()

            print(">> cur_section", cur_section)
            continue

        # swy: skip empty cells (again, but only check for hashcodes)
        if not row[MARKER_HASHCODE_COLUMN]:
            continue

        # swy: this string/row is marked as old/deprecated/dead/obsolete
        if row[DEAD_TEXT_COLUMN] and int(row[DEAD_TEXT_COLUMN]) == 1:
            continue

        # swy: get rid of strings that have been changed to "REMOVED"
        if row[MARKER_LANGUAGE_START_COLUMN + 1] and row[MARKER_LANGUAGE_START_COLUMN + 1] == "REMOVED":
            continue

        # swy: ignore beta/technical strings that are used but don't have/need translatable text:
        if row[MARKER_HASHCODE_COLUMN] in ignored_section_strings:
            print(" [i] ignoring %s" % row[MARKER_HASHCODE_COLUMN])
            continue

        # swy: export it in this 'simple' format:
        #      https://docs.transifex.com/formats/chrome-json
        out[row[MARKER_HASHCODE_COLUMN]] = collections.OrderedDict()

        out[row[MARKER_HASHCODE_COLUMN]]["message"]     = row[CUR_LANG_COLUMN]
        #out[row[MARKER_HASHCODE_COLUMN]]["description"] = "SphinxText.xls, row %u" % (i + 1) # swy: starts at zero

        #print("--", row[MARKER_HASHCODE_COLUMN])

        #print(row[MARKER_HASHCODE_COLUMN], row[CUR_LANG_COLUMN],  len(row))

#print(out)

# kwargs = {'newline': ''}
# mode = 'w'
# with open('test.csv', mode, **kwargs) as fp:
    # writer = csv.writer(fp, delimiter=',')
    # writer.writerows(data_read)