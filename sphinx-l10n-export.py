import csv

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


data_read = []

with open('SphinxTextFiltered.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    data_read = [row for row in reader]
    #print(data_read[35])

if (data_read[0][0] != "SHEET_TYPE_TEXT"):
    print("error: this needs to be a EuroLand text spreadsheet dump.")
    exit(-1)
    
# swy: programmatically find the correct indexes
for i, cur in enumerate(data_read):
    if len(cur) > 1 and cur[0] == "HEADER_ROW":
        HEADER_ROW = i
        break
        
print("head", HEADER_ROW)

MARKER_HASHCODE       = data_read[HEADER_ROW].index("MARKER_HASHCODE")
MARKER_LANGUAGE_START = data_read[HEADER_ROW].index("MARKER_LANGUAGE_START")
MARKER_LANGUAGE_END   = data_read[HEADER_ROW].index("MARKER_LANGUAGE_END")


print("INDEX THING", data_read[HEADER_ROW].index("MARKER_ENGLISH_UK"))

# for cur in data_read:
    # if (len(cur) > 3 and cur[3]=="HT_Text_Credits1"):
        # print(cur[5], len(cur))
    
kwargs = {'newline': ''}
mode = 'w'
with open('test.csv', mode, **kwargs) as fp:
    writer = csv.writer(fp, delimiter=',')
    writer.writerows(data_read)