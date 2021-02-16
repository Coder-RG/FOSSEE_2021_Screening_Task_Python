import sqlite3
import sys

#MVC: Model, View, Controller

#Model
class Model(Object):
    def __init__(self, dbname=None):
        self.dbname = dbname

    def connect_to_db(self):
        conn = sqlite3.connect(self.dbname)
        return conn

    def connect(func):
        def inner(self, conn, *args, **kwargs):
            try:
                conn.execute('SELECT name FROM sqlite_master WHERE type="table";')
            except:
                conn = self.connect_to_db()
            return func(self, conn, *args, **kwargs)
        return inner

#View
class View(Object):
    return

#Controller
class Controller(Object):
    return

if __name__ == '__main__':
    sys.exit(0)
