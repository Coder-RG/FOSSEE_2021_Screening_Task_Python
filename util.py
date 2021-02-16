import sqlite3
import view_database as vdb
import openpyxl
loc = ("new_sections.xlsx")

dbname = "steel_sections.sqlite"

class NotValidDB(Exception):
    pass

class ItemNotStored(Exception):
    pass

class ItemAlreadyStored(Exception):
    pass

class NotValidTable(Exception):
    pass

def start_connection():
    """Establish connection with Database"""
    global dbname
    conn = sqlite3.connect(dbname)
    return conn

def connect(func):
    def inner(conn, *args, **kwargs):
        query = 'SELECT name FROM sqlite_master WHERE type="table";'
        try:
            conn.execute(query)
        except Exception as e:
            conn = start_connection()
        return func(conn, dbname, *args, **kwargs)
    return inner

def end_connection(conn):
    return

@connect
def insert_one(conn, table_name, values):
    """Inserts data into table mentioned in the `table_name`"""
    if table_name == 'Beams':
        #20
        query = 'INSERT INTO Beams VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    elif table_name == 'Angles':
        #24
        query = 'INSERT INTO Angles VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    else:
        #21
        query = 'INSERT INTO Channels VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    conn.execute(query, values)
    # for row in conn.execute('SELECT * FROM {}'.format(table_name)):
    #     print(row)
    # conn.close()

@connect
def insert_many(conn, table_name, file_name):
    """Inserts data from Excel file(.xlsx) in the table"""
    if table_name == 'Beams':
        #20
        query = 'INSERT INTO Beams VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    elif table_name == 'Angles':
        #24
        query = 'INSERT INTO Angles VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    else:
        #21
        query = 'INSERT INTO Channels VALUES\
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'
    return

@connect
def view_all(conn, table_name):
    """View Table data of `table_name`"""
    if table_name is None:
        raise NotValidTable("Enter a valid table name")
    query = "SELECT * FROM {}".format(table_name)
    return conn.execute(query)

@connect
def view_one(conn, table_name, designation):
    if table_name is None:
        raise NotValidTable("Enter a valid table name")
    query = "SELECT * FROM {} WHERE designation=?".format(table_name)
    return conn.execute(query, (designation,))

@connect
def update_one(conn, table_name, designation, column_list):
    if table_name is None:
        raise NotValidTable("Enter a valid table name")
    query = "UPDATE {} SET ({})=({})\
    WHERE designation=?".format(table_name, column_list, values)
    return conn.execute(query, designation)

if __name__ == '__main__':
    conn = start_connection()
    for row in conn.execute('SELECT * FROM Beams;'):
        print(row)
    # end_connection(conn)
    # wb = openpyxl.load_workbook(loc)
    # sheet = wb.active
    # max_col = sheet.max_column
    # values = [sheet.cell(row=2, column=i).value for i in range(1, max_col+1)]
    # insert_into_table(None, 'steel_sections.sqlite', 'Beams', values)
