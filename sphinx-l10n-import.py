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
    'MARKER_GREEK':      'el',
    'MARKER_ARABIC':     'ar',
    'MARKER_RUSSIAN':    'ru',
    'MARKER_UKRAINIAN':  'uk',
}


ignored_section_markers = [ 'M_STATIC_TEXT' ]


data_read = []

# swy: parse the SphinxText.csv and load it as a row-major list
with open('SphinxText.csv', 'r', encoding='utf-8') as f:
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

MARKER_SRC_LANGUAGE_COLUMN   = MARKER_LANGUAGE_START_COLUMN + 1 # en_US; first language in the column range

for cur in lang:
    # swy: check that this spreadsheet actually contains a column for this language, it can happen
    if (cur not in data_read[HEADER_ROW]):
        print("warning: doesn't seem like this spreadsheet contains a %s; appending it..." % cur)
        
        # swy: iterate for all the rows; add a new blank column, shifting the rest a bit
        for i, row in enumerate(data_read):
            data_read[i].insert(MARKER_LANGUAGE_END_COLUMN, "")
            
        # swy: make a human-readable thingie from the marker tag (e.g. MARKER_ENGLISH_US -> English US)
        e = cur.replace("MARKER_", "").replace("_", " ").split(" ")
        e[0] = e[0][0] + e[0][1:].lower()
        
        # swy: add the correct marker into the new blank column so that Euroland can detect it properly, while
        #      the second line adds the readable language column tag; but keep in mind that is kind of hacky ¯\_(ツ)_/¯
        data_read[HEADER_ROW    ][MARKER_LANGUAGE_END_COLUMN] = cur
        data_read[HEADER_ROW - 1][MARKER_LANGUAGE_END_COLUMN] = " ".join(e)
        
        
    # swy: get the column index for the current language (important, we need
    #      to do it here because we may have added it just now)
    CUR_LANG_COLUMN = data_read[HEADER_ROW].index(cur)
    print(cur, lang[cur], "INDEX THING", CUR_LANG_COLUMN)
    
    # swy: reset the list of characters used in each language
    cur_glyphs = []
    
    # swy: reset the section and output data; once per language in the loop
    cur_section = ""
    cur_section_count = 0
    tx_json = collections.OrderedDict()

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
        if row[0] != "" and cur_section != row[0]: # and not row[0] in ignored_section_markers:
            print(">> pre_section", cur_section)
            cur_section = row[0];
            print(">> cur_section", cur_section)
            
            # swy: grab the correct JSON section file for the current language,
            # swy: imported from Transifex in this 'simple' format
            #      https://docs.transifex.com/formats/chrome-json
            file = "%s/%s.json" % (lang[cur], cur_section.replace("M_", "").lower())
            
            try:
                with open(file, 'r', encoding='utf-8') as outfile:
                    tx_json = json.load(outfile)
            except FileNotFoundError:
                print("warning: section file '%s' not found, skipping %s" % (file, cur_section))

            cur_section_count = cur_section_count + 1
            continue

        # swy: skip empty cells (again, but only check for hashcodes)
        if not row[MARKER_HASHCODE_COLUMN]:
            continue

        hashcode = row[MARKER_HASHCODE_COLUMN]

        # swy: if the translation string is not empty; index the JSON list 
        #      by its hashcode tag and access its sole "message" attribute

        if hashcode in tx_json:
            if tx_json[hashcode]["message"]:
                data_read[i][CUR_LANG_COLUMN] = tx_json[hashcode]["message"]
                cur_glyphs.extend(list(tx_json[hashcode]["message"]))
                
            else: # swy: empty/WIP/untranslated; use placeholder English text surrounded by asterisks for the time being. e.g: "**text*"
                data_read[i][CUR_LANG_COLUMN] = "**" + data_read[i][MARKER_SRC_LANGUAGE_COLUMN] + "*"
                
                
        # swy: by default we keep any original translations that aren't part of the JSON overrides,
        #      but if the translation field is missing or blank we use the raw en_US counterpart
        if not data_read[i][CUR_LANG_COLUMN]:
            data_read[i][CUR_LANG_COLUMN] = data_read[i][MARKER_SRC_LANGUAGE_COLUMN]
            
    # swy: get the list of combined characters for this language, de-duplicate them and sort :)
    cur_glyphs = list(dict.fromkeys(cur_glyphs))
    cur_glyphs.sort()
    print(cur_glyphs)
    
    # swy: we can use this in euroland to reduce the list of needed characters in our bitmap font to the bare minimum
    unicode = [ord(i) for i in cur_glyphs]
    unicode_str = ""
    range_start = -1
    for i, glyph in enumerate(unicode):
        if len(unicode) > i + 2 and glyph + 1 == unicode[i + 1]:
            if i < range_start or range_start == -1:
                range_start = i
        else:
            if range_start != -1:
                unicode_str += "%u-%u, " % (unicode[range_start], glyph)
                range_start = -1
            else:
                unicode_str += "%u, " % glyph
    print("\n[i] Unicode glyph ranges in use for %s: " % cur.split('_')[1].lower(), unicode_str.strip(' ,'))

with open('SphinxTextImported.csv', 'w', newline='', encoding='utf-8') as fp:
    writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(data_read)