import sys
import sqlite3
from PyQt5 import QtWidgets, QtSql, QtGui, QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QMessageBox, QInputDialog
from ui_main import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.actionOpen.triggered.connect(self.open_database)
        self.searchButton.clicked.connect(self.search_data)
        self.addButton.clicked.connect(self.add_data)
        self.editButton.clicked.connect(self.edit_data)
        self.deleteButton.clicked.connect(self.delete_data)
        self.tablesListWidget.itemClicked.connect(self.display_table)
        self.db = None

        self.set_logo("ishakpasa.jpeg")

    def set_logo(self, logo_path):
        pixmap = QtGui.QPixmap(logo_path)
        self.logoLabel.setPixmap(pixmap.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        self.logoLabel.setScaledContents(True)

    def open_database(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open SQLite Database", "", "SQLite Files (*.sqlite);;All Files (*)", options=options)
        if fileName:
            self.connect_to_database(fileName)

    def connect_to_database(self, db_file):
        if self.db:
            self.db.close()

        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(db_file)

        if not self.db.open():
            QMessageBox.critical(None, "Database Error", self.db.lastError().text())
            return

        self.update_table_list()

    def update_table_list(self):
        query = QtSql.QSqlQuery("SELECT name FROM sqlite_master WHERE type='table';", self.db)
        self.tablesListWidget.clear()
        while query.next():
            self.tablesListWidget.addItem(query.value(0))

    def display_table(self, item):
        table_name = item.text()
        model = QtSql.QSqlTableModel(self, self.db)
        model.setTable(table_name)
        model.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        model.select()
        self.tableView.setModel(model)

    def search_data(self):
        search_text = self.searchLineEdit.text()
        current_table = self.tablesListWidget.currentItem().text() if self.tablesListWidget.currentItem() else None
        if current_table:
            query = QtSql.QSqlQuery(f"SELECT * FROM {current_table} WHERE name LIKE '%{search_text}%'", self.db)
            model = QtSql.QSqlQueryModel()
            model.setQuery(query)
            self.tableView.setModel(model)

    def add_data(self):
        current_table = self.tablesListWidget.currentItem().text() if self.tablesListWidget.currentItem() else None
        if current_table:
            columns_query = QtSql.QSqlQuery(f"PRAGMA table_info({current_table})", self.db)
            columns = []
            while columns_query.next():
                columns.append(columns_query.value(1))
            data = []
            for col in columns:
                value, ok = QInputDialog.getText(self, "Add Data", f"Enter value for {col}:")
                if ok:
                    data.append(value)
                else:
                    return
            query = QtSql.QSqlQuery(self.db)
            query.prepare(f"INSERT INTO {current_table} ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})")
            for i, val in enumerate(data):
                query.bindValue(i, val)
            if not query.exec_():
                QMessageBox.critical(self, "Insert Error", query.lastError().text())
            else:
                self.display_table(self.tablesListWidget.currentItem())

    def edit_data(self):
        index = self.tableView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Edit Error", "Please select a cell to edit.")
            return
        new_value, ok = QInputDialog.getText(self, "Edit Data", "Enter new value:")
        if ok:
            model = self.tableView.model()
            model.setData(index, new_value)
            model.submitAll()

    def delete_data(self):
        index = self.tableView.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Delete Error", "Please select a row to delete.")
            return
        model = self.tableView.model()
        model.removeRow(index.row())
        model.submitAll()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
