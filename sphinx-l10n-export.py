import csv

# with open("SphinxTextFiltered.csv", mode="r", encoding="utf-8") as ins:
    # array = []
    # for line in ins:
        # array.append(line)
        # print(line.split(","))
data_read = []

with open('SphinxTextFiltered.csv', 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    data_read = [row for row in reader]
    #print(data_read[35])

print("INDEX THING",data_read[2].index("MARKER_ENGLISH_UK"))

# for cur in data_read:
    # if (len(cur) > 3 and cur[3]=="HT_Text_Credits1"):
        # print(cur[5], len(cur))
    
kwargs = {'newline': ''}
mode = 'w'
with open('test.csv', mode, **kwargs) as fp:
    writer = csv.writer(fp, delimiter=',')
    # writer.writerow(["your", "header", "foo"])  # write header
    writer.writerows(data_read)