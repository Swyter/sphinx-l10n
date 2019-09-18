import csv
import os
import json
import collections

HEADER_ROW = 3 - 1 # swy: the header row is usually in the third line (2 when indexing from zero)
MARKER_HASHCODE       = -1
MARKER_LANGUAGE_START = -1
MARKER_LANGUAGE_END   = -1

lang = {
    'MARKER_ENGLISH_US': 'en_UK',
    'MARKER_ENGLISH_UK': 'en_US',
    'MARKER_GERMAN':     'de',
    'MARKER_FRENCH':     'fr',
    'MARKER_SPANISH':    'es',
    'MARKER_ITALIAN':    'it',
    'MARKER_KOREAN':     'ko',
    'MARKER_JAPANESE':   'ja'
}

ignored_section_markers = [ 'M_STATIC_TEXT' ]


data_read = []

with open('SphinxText.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    data_read = [row for row in reader]
    #print(data_read[35])

if (data_read[0][0] != "SHEET_TYPE_TEXT"):
    print("error: this needs to be a EuroLand text spreadsheet dump.")
    exit(-1)
    
# swy: programmatically find the correct indexes
for i, row in enumerate(data_read):
    if len(row) > 1 and row[0] == "MARKER_FORMAT_ROW":
        HEADER_ROW = i
        break
        
print("head", HEADER_ROW)

MARKER_HASHCODE       = data_read[HEADER_ROW].index("MARKER_HASHCODE")
MARKER_LANGUAGE_START = data_read[HEADER_ROW].index("MARKER_LANGUAGE_START")
MARKER_LANGUAGE_END   = data_read[HEADER_ROW].index("MARKER_LANGUAGE_END")

cur_section = ""
out = collections.OrderedDict()

for cur in lang:
    cur_col_idx = data_read[HEADER_ROW].index(cur)
    print(cur, lang[cur], "INDEX THING", cur_col_idx)
    
    if not os.path.exists(lang[cur]):
        os.mkdir(lang[cur])

    for i, row in enumerate(data_read):
        # swy: skip empty rows
        if len(row) < 3:
            continue
        
        # swy: skip anything that goes before the actual table
        if i <= HEADER_ROW:
            continue
           
        # swy: skip empty cells
        if not row[0] and not row[MARKER_HASHCODE]:
            continue
        
        # swy: stop parsing once the table ends 
        if row[0] == "MARKER_LAST_MESSAGE":
            break
        
        if row[0] != "" and cur_section != row[0]: # and not row[0] in ignored_section_markers:
            cur_section = row[0];
            print(">> cur_section", cur_section)
            continue

        # swy: export it in this 'simple' format:
        #      https://docs.transifex.com/formats/chrome-json
        out[row[MARKER_HASHCODE]] = collections.OrderedDict()
        
        out[row[MARKER_HASHCODE]]["message"]     = row[cur_col_idx]
        out[row[MARKER_HASHCODE]]["description"] = "SphinxText.xls | Row: %u" % (i + 1)
            
        #print("--", row[MARKER_HASHCODE])
            
        #print(row[MARKER_HASHCODE], row[cur_col_idx],  len(row))
    break
        
print(out)

with open('data.json', 'w') as outfile:
    json.dump(out, outfile, indent=2)
    
kwargs = {'newline': ''}
mode = 'w'
with open('test.csv', mode, **kwargs) as fp:
    writer = csv.writer(fp, delimiter=',')
    writer.writerows(data_read)