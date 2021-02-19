import util
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
import view_database as vdb

#MVC: Model, View, Controller

#Model
class Model(object):
    def __init__(self, dbname=None):
        self.dbname = dbname
        self.conn = util.start_connection()

    def insert_data(self, table, values):
        util.insert_one(self.conn, table, values)

    def view_row(self, table, designation):
        util.view_one(self.conn, table, designation)

    def view_table(self, table):
        return util.view_all(self.conn, table)

    def get_columns(self, table):
        return vdb.get_columns(self.dbname, table)

#View/Controller
class View(QMainWindow):
    def __init__(self, Model):
        super(View, self).__init__()
        self.model = Model
        loadUi("/home/rishabh/project/untitled.ui", self)
        self.category = ("I/Beam", "Angles", "Channels")
        self.handle_stackedWidget()
        self.handle_combobox()

    def handle_stackedWidget(self):
        self.stackedWidget.setCurrentIndex(0)
        self.add_item.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.view_item.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.view_tables.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

    def handle_combobox(self):
        self.add_item_combobox.addItems(self.category)
        self.view_tables_combobox.addItems(self.category)
        # self.view_item_combobox.addItems()
        self.add_item_combobox.activated.connect(self.func_add_item)
        self.view_tables_combobox.activated.connect(self.func_view_table)
        # self.submit.clicked.connect(self.func_add_item)

    def func_add_item(self):
        option = self.add_item_combobox.currentText()
        if option == "I/Beam":
            option = "Beams"
        header = self.model.get_columns(option)
        self.add_item_table.setColumnCount(20)
        self.add_item_table.setHorizontalHeaderLabels(header)
        self.add_item_table.setRowCount(1)

    def func_view_item(self):
        pass

    def func_view_table(self):
        option = self.view_tables_combobox.currentText()
        if option == "I/Beam":
            option = "Beams"
        header = self.model.get_columns(option)
        data = self.model.view_table(option)
        self.view_table_table.setColumnCount(len(header))
        self.view_table_table.setHorizontalHeaderLabels(header)
        self.view_table_table.setRowCount(1)
        index = 0
        for row in data:
            for col in range(len(header)):
                self.view_table_table.setItem(index, col, QtWidgets.QTableWidgetItem(str(row[col])))
            index += 1
            self.view_table_table.insertRow(self.view_table_table.rowCount())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = View(Model('steel_sections.sqlite'))
    main_window.show()
    sys.exit(app.exec_())
