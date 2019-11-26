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


ignored_section_markers = [ 'M_STATIC_TEXT' ]


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
    #CUR_LANG_COLUMN = data_read[HEADER_ROW].index(cur)
    #print(cur, lang[cur], "INDEX THING", CUR_LANG_COLUMN)
    # swy: check that this spreadsheet actually contains a column for this language, it can happen
    if (cur not in data_read[HEADER_ROW]):
        print("warning: doesn't seem like this spreadsheet contains a %s; appending it..." % cur)
        
        # swy: iterate for all the rows; add a new blank column, shifting the rest a bit
        for i, row in enumerate(data_read):
            data_read[i].insert(MARKER_LANGUAGE_END_COLUMN, "")
            
        # swy: make a human-readable thingie from the marker tag (e.g. MARKER_ENGLISH_US -> English US)
        e = cur.replace("MARKER_", "").replace("_", " ").split(" ")
        e[0] = e[0][0] + e[0][1:].lower()
        
        data_read[HEADER_ROW    ][MARKER_LANGUAGE_END_COLUMN] = cur
        data_read[HEADER_ROW - 1][MARKER_LANGUAGE_END_COLUMN] = " ".join(e)
        #data_read[HEADER_ROW][MARKER_LANGUAGE_END_COLUMN] = data_read[HEADER_ROW][MARKER_LANGUAGE_END_COLUMN] + 1
        
        
    # swy: get the column index for the current language
    CUR_LANG_COLUMN = data_read[HEADER_ROW].index(cur)
    print(cur, lang[cur], "INDEX THING", CUR_LANG_COLUMN)
    
    
    # swy: reset the section and output data; once per language in the loop
    cur_section = ""
    cur_section_count = 0
    out = collections.OrderedDict()

    # swy: iterate for all the rows, once per language
    for i, row in enumerate(data_read):
    
        # print("a")
        # print(row)
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
            print(">> pre_section", cur_section)
            
            file = "%s/%s.json" % (lang[cur], cur_section.replace("M_", "").lower())
            
            try:
                with open(file, 'r') as outfile:
                    out = json.load(outfile)
            except FileNotFoundError:
                print("section file '%s' not found, skipping %s" % (file, cur_section))

            cur_section_count = cur_section_count + 1

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
            
            
        data_read[i][CUR_LANG_COLUMN] = out[ row[MARKER_HASHCODE_COLUMN] ]["message"]
        # print( out[ row[MARKER_HASHCODE_COLUMN] ]["message"])
            

        # swy: export it in this 'simple' format:
        #      https://docs.transifex.com/formats/chrome-json
        out[row[MARKER_HASHCODE_COLUMN]] = collections.OrderedDict()

        out[row[MARKER_HASHCODE_COLUMN]]["message"]     = row[CUR_LANG_COLUMN]
        #out[row[MARKER_HASHCODE_COLUMN]]["description"] = "SphinxText.xls, row %u" % (i + 1) # swy: starts at zero

        #print("--", row[MARKER_HASHCODE_COLUMN])

        #print(row[MARKER_HASHCODE_COLUMN], row[CUR_LANG_COLUMN],  len(row))

with open('test.csv', 'w', newline='') as fp:
    writer = csv.writer(fp, delimiter=',', quoting=csv.QUOTE_MINIMAL)
    writer.writerows(data_read)