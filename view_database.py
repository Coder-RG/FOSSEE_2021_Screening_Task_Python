#!/usr/bin/env python3
import sqlite3
import sys

def display_schema(dbname):
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

if __name__ == '__main__':
    name = sys.argv[1]
    display_schema(name)
