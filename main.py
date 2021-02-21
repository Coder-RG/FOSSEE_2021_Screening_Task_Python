import util
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow
# import view_database as vdb

#MVC: Model, View, Controller

#Model
class Model(object):
    """All the relevant methods for interacting with the database reside here.
    This is, therefore, the Model part in the MVC architecture"""
    def __init__(self, dbname=None):
        self.dbname = dbname
        self.conn = util.start_connection()

    def insert_data(self, table, values):
        util.insert_one(self.conn, table, values)

    def view_row(self, table, designation):
        return util.view_one(self.conn, table, designation).fetchone()

    def view_table(self, table):
        return util.view_all(self.conn, table)

    def get_designations(self, table):
        return util.get_designations(self.conn, table)

    def get_columns(self, table):
        return util.get_columns(self.conn, table)

    def get_id(self, table):
        return util.get_Id(self.conn, table)

#View/Controller
class View(QMainWindow):
    """All the necessary code for the GUI of the application. Coinicidentally,
    this is also the View and Controller for the application."""
    def __init__(self, Model):
        super(View, self).__init__()
        self.model = Model
        loadUi("/home/rishabh/project/untitled.ui", self)
        self.setWindowIcon(QtGui.QIcon('beam2.png'))
        self.category = ("I/Beam", "Angles", "Channels")
        self.designation = None
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
        self.view_item_combobox1.addItems(self.category)
        self.add_item_combobox.activated.connect(self.func_add_item)
        self.view_tables_combobox.activated.connect(self.func_view_table)
        self.view_item_combobox1.activated[str].connect(self.abc)
        self.submit.clicked.connect(self.func_add_item_data)

    def func_add_item_data(self):
        row_val = list()
        for col in range(self.header_length-1):
            col_val = self.add_item_table.item(0, col)
            if col_val is None:
                row_val.append(None)
            else:
                row_val.append(col_val.text())
        print(row_val)

    #Populate the table widget for the add_item stack
    def func_add_item(self):
        option = self.add_item_combobox.currentText()
        if option == "I/Beam":
            option = "Beams"
        header = self.model.get_columns(option)
        self.header_length = len(header)
        self.add_item_table.setColumnCount(self.header_length-1)
        self.add_item_table.setHorizontalHeaderLabels(header[1:])
        self.add_item_table.setRowCount(1)

    #Populate the table widget for the view_item stack
    def abc(self):
        option = self.view_item_combobox1.currentText()
        if option == "I/Beam":
            option = "Beams"
        result = self.model.get_designations(option)
        self.view_item_combobox2.clear()
        self.view_item_combobox2.addItems(result)
        self.view_item_combobox2.activated[str].connect(self.xyz)

    def xyz(self):
        option = self.view_item_combobox1.currentText()
        if option == "I/Beam":
            option = "Beams"
        designation = self.view_item_combobox2.currentText()
        #This function is being called multiple times(don't know why)
        #so to avoid this, this if cond is implemented.
        if self.designation != designation:
            header = self.model.get_columns(option)
            self.designation = designation
            result = self.model.view_row(option, designation)
            self.view_item_table.setColumnCount(len(result)-1)
            self.view_item_table.setHorizontalHeaderLabels(header[1:])
            self.view_item_table.setRowCount(1)
            for col in range(1, len(result)):
                self.view_item_table.setItem(0, col-1, QtWidgets.QTableWidgetItem(str(result[col])))

    #Populate the table widget for the view_table stack
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
        self.view_table_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = View(Model('steel_sections.sqlite'))
    main_window.show()
    sys.exit(app.exec_())
