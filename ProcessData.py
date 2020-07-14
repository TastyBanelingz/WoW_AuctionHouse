
#
#   This is the script that reads the RawData.txt file, cleans it
#   and then writes to a CSV as well as appends it to the SQL database wowAH.db
#

# TODO:
import os
import AHutils

#Clean data from lua retrieval script
f = open("Data/Temp/RawData.txt", 'r')

contents = f.read()

contents = contents.replace('},{', '}\n{')
contents = contents.replace('return {', '')
contents = contents.replace('{"|', '')
contents = contents.replace('"|', '')
contents = contents.replace('",', ',')
contents = contents.replace(',"', ',')
contents = contents.replace('}', '')
contents = contents.replace(',,,', ',,')
f.close()

f = open("Data/Temp/ProcessedData.txt", 'w')
f.write(contents)
f.close()

with open("Data/Temp/ProcessedData.txt", 'r') as f:
    x = 0
    data = []
    for line in f:
        x = x + 1
        linesplit = line.split(',')
        data.append(linesplit)
    
f = open("Data/Temp/ProcessedData.txt", 'w')

#Connect to SQLite DB
print("Connecting to SQLite database...")
conn = AHutils.sqlite3.connect('Data/Database/wowAH.db')
AHutils.db_CreateTable_AH_Data(conn, 'AH_data')

c = conn.cursor()

#clear out prior entries for same days
sources = (AHutils.unique2(data, 28))

for y in sources:
    AHutils.db_ClearDataByFilesource(conn, 'AH_data', y)

#load the data to database and to CSV
for x in data:
    
    #Handles Firework and Gurubashi book instances
    #only sellable items with and additional comma in the name
    if len(x) >= 31:
        x.pop(1)
        itemName = x[8] + ',' + x[9]
        x.pop(9)
    else:
        itemName = x[8]
    
    stackSize = int(float(x[10]))
    bidPrice = int(x[14])
    buyPrice = int(x[16])
    seller = x[19]
    ppuBid = int(round(bidPrice / stackSize, 0))
    ppuBuy = int(round(buyPrice / stackSize , 0))
    fileSource = x[28]
    scanDate = x[28][13:-12]
    scanTime = x[28][-11:-5]


    #UnkownSeller marks entries with no seller.
    #these seem to be bad and can be ignored
    #visual and manual validation was done to come to this conclusion.
    if len(seller) > 0:
        #CSV
        f.write(itemName + '|' + str(stackSize) + '|' + str(bidPrice) + '|' + str(buyPrice) + '|' + seller + '|' + str(ppuBid) + '|' + str(ppuBuy) +  '|' + scanDate + '|' + scanTime + '|' + fileSource)
        #SQL
        c.execute("INSERT INTO AH_data VALUES (?,?,?,?,?,?,?,?,?,?,?)",(None,itemName,stackSize,bidPrice,buyPrice,seller,ppuBid,ppuBuy,scanDate,scanTime,fileSource))

AHutils.db_CleanEscapeChars(conn)

os.unlink('./Data/Temp/RawData.txt')
os.unlink('./Data/Temp/ProcessedData.txt')

conn.commit()
conn.close()
f.close()

