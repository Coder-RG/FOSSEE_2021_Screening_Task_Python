#!/usr/bin/env python3
import sqlite3
import sys

def display_db_schema(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    )
    result = c.fetchall()
    for x in result:
        print("\n{} Schema\n".format(x[0]))
        for row in c.execute("PRAGMA table_info({})".format(x[0])):
            print(row)
    c.close()

def display_table_schema(dbname, table_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for row in c.execute('PRAGMA table_info="{}"'.format(table_name)):
        print(row)
    c.close()

def display_table_rowcount(dbname, table_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    c.execute(
        'Select COUNT(*) FROM "{}"'.format(table_name)
    )
    print("No of rows: ", c.fetchall())
    c.close()

def display_table_data(dbname, table_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    for row in c.execute('Select * FROM "{}"'.format(table_name)):
        print(row)
    c.close()

def get_columns(dbname, table_name):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    column_names = list()
    for row in c.execute('PRAGMA table_info="{}"'.format(table_name)):
        column_names.append(row[1])
    return column_names

if __name__ == '__main__':
    option = sys.argv[1]
    dbname = input("Enter the db name: ")
    table_name = input("Enter the table name: ")
    if option == '0':
        print(get_columns(dbname, table_name))
    else:
        if input("Display Schema?") == 'y':
            display_table_schema(dbname, table_name)
        while(table_name != 'q'):
            if input("Display rowcount?") == 'y':
                display_table_rowcount(dbname, table_name)
            elif input("Display data?") == 'y':
                display_table_data(dbname, table_name)
            table_name = input("Enter the table name or quit(q): ")
