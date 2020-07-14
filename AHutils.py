import pandas 
import sqlite3

def unique(list1): 
    unique_list = [] 
    for x in list1: 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

def unique2(listoflists, pos): 
    unique_list = [] 
    for x in listoflists: 
        val = x[pos].replace('\n', '')
        if val not in unique_list and len(val) > 0: 
            unique_list.append(val) 
        if len(unique_list) > 10000:
            #print(unique_list)
            break
    return unique_list

def db_ClearDataByDates(connection, table ,dateToBeDeleted):
    c = connection.cursor()
    c.execute("DELETE FROM  " + table + " where  scanDate = " + dateToBeDeleted)
    connection.commit()
    
def db_ClearDataByFilesource(connection, table ,sourcefile):
    c = connection.cursor()
    print("DELETE FROM  " + table + " where  sourcefile like '" + sourcefile[:-4] + "%'")
    c.execute("DELETE FROM  " + table + " where  sourcefile like '" + sourcefile[:-4] + "%'")
    connection.commit()

def db_ClearTable(connection, table):
    c = connection.cursor()
    print("DELETE FROM  " + table + " where  1 = 1")
    c.execute("DELETE FROM  " + table + " where  1 = 1")
    connection.commit()

def db_CleanEscapeChars(connection):
    c = connection.cursor()
    c.execute("update AH_data set itemName = replace(itemName, '\\', '')")
    connection.commit()

def db_DropTable(connection, table):
    c.executescript('DROP TABLE IF EXISTS '+ table + ';')
    print(table + ' Table Dropped')

def db_CreateTable_AH_Data(connection, table):
    c = connection.cursor()
    c.execute('''CREATE TABLE if not exists AH_data (
        id   INTEGER       UNIQUE
                        PRIMARY KEY
                        NOT NULL,
    itemName VARCHAR (255),
    stackSize INTEGER,
    bidPrice INTEGER,
    buyPrice INTEGER,
    seller VARCHAR (255),
    bidPPU INTEGER,
    buyPPU INTEGER,
    scanDate VARCHAR (8),
    scanTime VARCHAR (6),
    sourcefile VARCHAR (255)
    );''')
    connection.commit()

def db_Query_ItemSummary(connection, ItemName = None, dt_from = None, dt_to = None):
    '''
    Query funciton to return summary of items from primary data table
    Can be run with no params, but will return every row

    Params:
    ItemName
    dt_from
    dt_to

    Returns list of rows
    '''
    c = connection.cursor()
    baseQuery = '''select 
            itemname Item,
            substr(scanDate, 1,4)|| '-' || substr(scanDate, 5,2) || '-' || substr(scanDate, 7,2)   Date, 
            min(buyPPU) MinBuy,
            round(avg(buyPPU), 0) AvgBuy,
            count(*) Volume
            from AH_data'''
    if ItemName or dt_from or dt_to:
        baseQuery = baseQuery + '\nwhere 1=1'

    if ItemName:
        baseQuery = baseQuery + "\nand itemname = '%s' " % (ItemName)

    if dt_from:
        baseQuery = baseQuery + "\nand scanDate >= '%s' " % (dt_from)
    
    if dt_from:
        baseQuery = baseQuery + "\nand scanDate <= '%s' " % (dt_to)

    query = baseQuery +   '''
            and buyPPU > 0
            group by itemname, scanDate
            order by 1, 2 asc;'''

    #c.execute(query)
    #items = c.fetchall()

    return query


def db_Query_SellerSummary(connection, ItemName = None, dt_from = None, dt_to = None):
    '''
    Query funciton to return summary of sellers from primary data table
    Can be run with no params, but will return every row

    Params:
    ItemName
    dt_from
    dt_to

    Returns list of rows
    '''
    c = connection.cursor()
    baseQuery = '''select 
            seller seller,
            substr(scanDate, 1,4)|| '-' || substr(scanDate, 5,2) || '-' || substr(scanDate, 7,2)   Date, 
            min(buyPPU) MinBuy,
            round(avg(buyPPU), 0) AvgBuy,
            count(*) Volume
            from AH_data'''
    if ItemName or dt_from or dt_to:
        baseQuery = baseQuery + '\nwhere 1=1'

    if ItemName:
        baseQuery = baseQuery + "\nand itemname = '%s' " % (ItemName)

    if dt_from:
        baseQuery = baseQuery + "\nand scanDate >= '%s' " % (dt_from)
    
    if dt_from:
        baseQuery = baseQuery + "\nand scanDate <= '%s' " % (dt_to)

    query = baseQuery +   '''
            and buyPPU > 0
            group by seller, scanDate
            order by 1, 2 asc;'''

    #c.execute(query)
    #items = c.fetchall()

    return query