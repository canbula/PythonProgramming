import sys
import sqlite3
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableWidget, QTableWidgetItem, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QInputDialog, QHBoxLayout, QTextEdit, QTabWidget, QFileDialog

class DataConnect:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)  # SQLite veritabanına bağlan
        self.cursor = self.conn.cursor()  # Bir cursor oluştur
        self.selected_table = None  # Başlangıçta seçili bir tablo yok

    def execute_query(self, query):
        # Veritabanında bir SQL sorgusu çalıştır
        try:
            self.cursor.execute(query)  # Sorguyu çalıştır
            self.conn.commit()  # Değişiklikleri kaydet
            result = self.cursor.fetchall()  # Tüm sonuçları al
            return 'Sorgu başarıyla çalıştırıldı.', result
        except Exception as e:
            return f'Hata: {str(e)}', []

    def select_table(self, table_name):
        # Bir tabloyu seç
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
            result = self.cursor.fetchone()  # İlk sonucu al
            if result:
                self.selected_table = table_name  # Tabloyu seç
                return f"'{table_name}' tablosu seçildi."
            else:
                return f"'{table_name}' adında bir tablo bulunamadı."
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_all_tables(self):
        # Tüm tablo isimlerini al
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            result = self.cursor.fetchall()  # Tüm sonuçları al
            return [table[0] for table in result]  # Tablo isimlerinin listesini döndür
        except Exception as e:
            return f'Hata: {str(e)}'

    def show_selected_table(self):
        # Seçili tabloyu göster
        if self.selected_table:
            try:
                self.cursor.execute(f"SELECT * FROM {self.selected_table}")
                result = self.cursor.fetchall()  # Tüm sonuçları al
                return result
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def add_data(self, **field_values):
        # Seçili tabloya veri ekle
        if self.selected_table:
            try:
                columns = ', '.join(field_values.keys())  # Sütun isimlerini birleştir
                placeholders = ', '.join(['?'] * len(field_values))  # Yer tutucular oluştur
                query = f"INSERT INTO {self.selected_table} ({columns}) VALUES ({placeholders})"
                self.cursor.execute(query, tuple(field_values.values()))  # Veriyi ekle
                self.conn.commit()  # Değişiklikleri kaydet
                return 'Veri başarıyla eklendi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def update_data(self, id, **field_values):
        # Seçili tablodaki veriyi güncelle
        if self.selected_table:
            try:
                placeholders = ', '.join([f"{k} = ?" for k in field_values.keys()])  # Yer tutucular oluştur
                query = f"UPDATE {self.selected_table} SET {placeholders} WHERE id = ?"
                values = tuple(field_values.values()) + (id,)  # Güncellenmiş değerler
                self.cursor.execute(query, values)  # Veriyi güncelle
                self.conn.commit()  # Değişiklikleri kaydet
                return 'Veri başarıyla güncellendi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def delete_data_by_row(self, row_num):
        # Seçili tablodaki bir satırı sil
        if self.selected_table:
            try:
                self.cursor.execute(f"DELETE FROM {self.selected_table} WHERE rowid = ?", (row_num,))
                self.conn.commit()  # Değişiklikleri kaydet
                return 'Veri başarıyla silindi.'
            except Exception as e:
                return f'Hata: {str(e)}'
        else:
            return "Lütfen önce bir tablo seçin."

    def create_table(self, table_name, **columns):
        # Yeni bir tablo oluştur
        try:
            columns_def = ', '.join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])  # Sütun tanımları oluştur
            self.cursor.execute(f"CREATE TABLE {table_name} ({columns_def})")  # Tabloyu oluştur
            self.conn.commit()  # Değişiklikleri kaydet
            return f"'{table_name}' tablosu başarıyla oluşturuldu."
        except Exception as e:
            return f'Hata: {str(e)}'

    def delete_table(self, table_name):
        # Bir tabloyu sil
        try:
            self.cursor.execute(f"DROP TABLE IF EXISTS {table_name}")  # Tabloyu sil
            self.conn.commit()  # Değişiklikleri kaydet
            return f"'{table_name}' tablosu başarıyla silindi."
        except Exception as e:
            return f'Hata: {str(e)}'

    def get_table_columns(self, table_name):
        # Bir tablodaki sütun isimlerini al
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            result = self.cursor.fetchall()  # Tüm sonuçları al
            return [column[1] for column in result]  # Sütun isimlerinin listesini döndür
        except Exception as e:
            return f'Hata: {str(e)}'

    def __del__(self):
        self.conn.close()  # Nesne silindiğinde bağlantıyı kapat

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SQLite Database Browser")  # Pencere başlığını ayarla
        self.setGeometry(100, 100, 600, 400)  # Pencere boyutunu ve konumunu ayarla
        self.setWindowIcon(QIcon(r'C:\Users\cengh\Desktop\Yeni klasör\DataConnect-\icon.png'))  # Pencereye logo ekle (Logo dosyasının yolu)

        self.main_layout = QVBoxLayout()  # Ana dikey yerleşim

        self.db_selection_layout = QVBoxLayout()  # Veritabanı seçim yerleşimi

        self.db_name_input = QLineEdit()  # Veritabanı adı girişi
        self.db_name_input.setPlaceholderText("Enter database name or select an existing file")

        select_db_button = QPushButton("Select Database")  # Veritabanı seçme butonu
        select_db_button.clicked.connect(self.select_database)

        create_db_button = QPushButton("Create Database")  # Veritabanı oluşturma butonu
        create_db_button.clicked.connect(self.create_database)

        self.db_selection_layout.addWidget(QLabel("Database Operations"))
        self.db_selection_layout.addWidget(self.db_name_input)
        self.db_selection_layout.addWidget(select_db_button)
        self.db_selection_layout.addWidget(create_db_button)

        self.main_layout.addLayout(self.db_selection_layout)  # Veritabanı seçim yerleşimini ana yerleşime ekle

        self.tabs = QTabWidget()  # Sekme widget'ı oluştur
        self.main_layout.addWidget(self.tabs)  # Sekmeleri ana yerleşime ekle

        self.setLayout(self.main_layout)  # Ana yerleşimi pencereye uygula

        self.setStyleSheet("""
            QWidget {
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                padding: 10px;
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QTableWidget {
                border: 1px solid #ccc;
            }
            QTabWidget::pane {
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QTabBar::tab {
                padding: 10px;
            }
            QTabBar::tab:selected {
                background-color: #007BFF;
                color: white;
            }
        """)

    def select_database(self):
        # Var olan bir veritabanını seç
        db_name, _ = QFileDialog.getOpenFileName(self, "Select Database", "", "SQLite Files (*.db *.sqlite)")
        if db_name:
            self.db_name_input.setText(db_name)
            self.init_db(db_name)

    def create_database(self):
        # Yeni bir veritabanı oluştur
        db_name = self.db_name_input.text()
        if not db_name:
            QMessageBox.warning(self, "Input Error", "Please enter a database name")
            return

        if not db_name.endswith('.db'):
            db_name += '.db'

        self.init_db(db_name)

    def init_db(self, db_name):
        # Veritabanını başlat
        self.db = DataConnect(db_name)  # Veritabanı bağlantısını başlat

        self.create_table_page = self.create_table_ui()  # Tablo oluşturma ve silme arayüzü
        self.table_operations_page = self.table_operations_ui()  # Tablo işlemleri arayüzü
        self.query_execution_page = self.query_execution_ui()  # Sorgu çalıştırma arayüzü

        self.tabs.clear()  # Sekmeleri temizle
        self.tabs.addTab(self.create_table_page, "Table Operations")  # Sekmeye tablo işlemleri arayüzünü ekle
        self.tabs.addTab(self.table_operations_page, "Data Operations")  # Sekmeye veri işlemleri arayüzünü ekle
        self.tabs.addTab(self.query_execution_page, "Execute Query")  # Sekmeye sorgu çalıştırma arayüzünü ekle

    def create_table_ui(self):
        # Tablo oluşturma ve silme arayüzünü oluştur
        widget = QWidget()
        layout = QVBoxLayout()

        self.table_name_input = QLineEdit()  # Tablo adı girişi
        self.table_name_input.setPlaceholderText("Table Name")

        self.columns_input = QLineEdit()  # Sütunlar girişi
        self.columns_input.setPlaceholderText("Columns (e.g. id INTEGER PRIMARY KEY, name TEXT)")

        create_table_button = QPushButton("Create Table")  # Tablo oluşturma butonu
        create_table_button.clicked.connect(self.create_table)

        delete_table_button = QPushButton("Delete Table")  # Tablo silme butonu
        delete_table_button.clicked.connect(self.delete_table)

        layout.addWidget(QLabel("Create a new table"))
        layout.addWidget(self.table_name_input)
        layout.addWidget(self.columns_input)
        layout.addWidget(create_table_button)
        layout.addWidget(delete_table_button)

        self.table_list = QListWidget()  # Var olan tabloların listesi
        self.table_list.itemClicked.connect(self.select_table)

        layout.addWidget(QLabel("Existing Tables"))
        layout.addWidget(self.table_list)

        show_tables_button = QPushButton("Show Tables")  # Tabloları göster butonu
        show_tables_button.clicked.connect(self.show_tables)

        layout.addWidget(show_tables_button)

        widget.setLayout(layout)  # Yerleşimi widget'a uygula

        return widget

    def create_table(self):
        # Yeni bir tablo oluştur
        table_name = self.table_name_input.text()
        columns = self.columns_input.text()

        if not table_name or not columns:
            QMessageBox.warning(self, "Input Error", "Table name and columns are required")
            return

        columns_dict = {col.split()[0]: col.split()[1] for col in columns.split(', ')}
        message = self.db.create_table(table_name, **columns_dict)
        QMessageBox.information(self, "Create Table", message)
        self.show_tables()

    def delete_table(self):
        # Bir tabloyu sil
        table_name = self.table_name_input.text()

        if not table_name:
            QMessageBox.warning(self, "Input Error", "Table name is required")
            return

        message = self.db.delete_table(table_name)
        QMessageBox.information(self, "Delete Table", message)
        self.show_tables()

    def show_tables(self):
        # Tüm tabloları göster
        tables = self.db.get_all_tables()
        self.table_list.clear()
        if isinstance(tables, list):
            self.table_list.addItems(tables)
        else:
            QMessageBox.warning(self, "Error", tables)

    def select_table(self, item):
        # Bir tabloyu seç
        table_name = item.text()
        message = self.db.select_table(table_name)
        QMessageBox.information(self, "Select Table", message)
        self.tabs.setCurrentWidget(self.table_operations_page)  # Veri işlemleri sekmesine geç

    def table_operations_ui(self):
        # Tablo işlemleri arayüzünü oluştur
        widget = QWidget()
        layout = QVBoxLayout()

        self.operation_status = QLabel("Table Operations")

        self.add_data_button = QPushButton("Add Data")  # Veri ekleme butonu
        self.add_data_button.clicked.connect(self.add_data_dialog)

        self.show_table_button = QPushButton("Show Table Contents")  # Tablo içeriğini gösterme butonu
        self.show_table_button.clicked.connect(self.show_table_contents)

        self.update_data_button = QPushButton("Update Data")  # Veri güncelleme butonu
        self.update_data_button.clicked.connect(self.update_data_dialog)

        self.delete_data_button = QPushButton("Delete Data")  # Veri silme butonu
        self.delete_data_button.clicked.connect(self.delete_data_dialog)

        self.table_content_display = QTableWidget()  # Tablo içeriği görüntüleme widget'ı

        layout.addWidget(self.operation_status)
        layout.addWidget(self.add_data_button)
        layout.addWidget(self.update_data_button)
        layout.addWidget(self.delete_data_button)
        layout.addWidget(self.show_table_button)
        layout.addWidget(self.table_content_display)

        back_button = QPushButton("Back to Main")  # Ana sayfaya dönüş butonu
        back_button.clicked.connect(self.back_to_main)

        layout.addWidget(back_button)

        widget.setLayout(layout)  # Yerleşimi widget'a uygula

        return widget

    def add_data_dialog(self):
        # Veri ekleme diyaloğunu aç
        column_names = self.db.get_table_columns(self.db.selected_table)
        if column_names:
            rows, ok = QInputDialog.getInt(self, "Add Data", "Enter number of rows:")  # Kaç satır ekleneceğini sor
            if ok:
                cols, ok = QInputDialog.getInt(self, "Add Data", "Enter number of columns:")  # Kaç sütun ekleneceğini sor
                if ok:
                    self.data_input_table = QTableWidget(rows, cols)
                    self.data_input_table.setHorizontalHeaderLabels(column_names[:cols])
                    
                    save_button = QPushButton("Save Data")  # Veriyi kaydet butonu
                    save_button.clicked.connect(self.save_data)

                    layout = QVBoxLayout()
                    layout.addWidget(self.data_input_table)
                    layout.addWidget(save_button)

                    data_input_dialog = QWidget()
                    data_input_dialog.setLayout(layout)
                    data_input_dialog.setGeometry(150, 150, 400, 300)
                    data_input_dialog.show()
                    self.data_input_dialog = data_input_dialog
        else:
            QMessageBox.warning(self, "Error", "No table selected")

    def update_data_dialog(self):
        # Veri güncelleme diyaloğunu aç
        column_names = self.db.get_table_columns(self.db.selected_table)
        if column_names:
            id, ok = QInputDialog.getInt(self, "Update Data", "Enter ID of the row to update:")  # Güncellenecek satırın ID'sini sor
            if ok:
                self.data_input_table = QTableWidget(1, len(column_names))
                self.data_input_table.setHorizontalHeaderLabels(column_names)
                
                save_button = QPushButton("Update Data")  # Veriyi güncelle butonu
                save_button.clicked.connect(lambda: self.update_data(id))

                layout = QVBoxLayout()
                layout.addWidget(self.data_input_table)
                layout.addWidget(save_button)

                data_input_dialog = QWidget()
                data_input_dialog.setLayout(layout)
                data_input_dialog.setGeometry(150, 150, 400, 300)
                data_input_dialog.show()
                self.data_input_dialog = data_input_dialog
        else:
            QMessageBox.warning(self, "Error", "No table selected")

    def delete_data_dialog(self):
        # Veri silme diyaloğunu aç
        row_num, ok = QInputDialog.getInt(self, "Delete Data", "Enter row number to delete:")  # Silinecek satır numarasını sor
        if ok:
            message = self.db.delete_data_by_row(row_num)
            QMessageBox.information(self, "Delete Data", message)
            self.show_table_contents()

    def save_data(self):
        # Veriyi kaydet
        rows = self.data_input_table.rowCount()
        cols = self.data_input_table.columnCount()
        data = []
        for row in range(rows):
            row_data = {}
            for col in range(cols):
                item = self.data_input_table.item(row, col)
                if item is not None:
                    row_data[self.data_input_table.horizontalHeaderItem(col).text()] = item.text()
            data.append(row_data)

        for row_data in data:
            message = self.db.add_data(**row_data)
            QMessageBox.information(self, "Add Data", message)

        self.data_input_dialog.close()
        self.show_table_contents()

    def update_data(self, id):
        # Veriyi güncelle
        cols = self.data_input_table.columnCount()
        row_data = {}
        for col in range(cols):
            item = self.data_input_table.item(0, col)
            if item is not None:
                row_data[self.data_input_table.horizontalHeaderItem(col).text()] = item.text()

        message = self.db.update_data(id, **row_data)
        QMessageBox.information(self, "Update Data", message)

        self.data_input_dialog.close()
        self.show_table_contents()

    def show_table_contents(self):
        # Tablo içeriğini göster
        table_contents = self.db.show_selected_table()
        if isinstance(table_contents, list):
            num_rows = len(table_contents)
            if num_rows > 0:
                num_cols = len(table_contents[0])
                self.table_content_display.setRowCount(num_rows)
                self.table_content_display.setColumnCount(num_cols)
                for i in range(num_rows):
                    for j in range(num_cols):
                        item = QTableWidgetItem(str(table_contents[i][j]))
                        self.table_content_display.setItem(i, j, item)
            else:
                self.table_content_display.setRowCount(0)
                self.table_content_display.setColumnCount(0)
        else:
            QMessageBox.warning(self, "Error", table_contents)

    def back_to_main(self):
        # Ana sayfaya dön
        self.tabs.setCurrentWidget(self.create_table_page)

    def query_execution_ui(self):
        # Sorgu çalıştırma arayüzünü oluştur
        widget = QWidget()
        layout = QVBoxLayout()

        self.query_input = QTextEdit()  # Sorgu girişi
        self.query_input.setPlaceholderText("Enter your SQL query here...")

        execute_query_button = QPushButton("Execute Query")  # Sorguyu çalıştırma butonu
        execute_query_button.clicked.connect(self.execute_query)

        self.query_result_display = QTableWidget()  # Sorgu sonuçlarını gösterme widget'ı

        layout.addWidget(QLabel("Execute SQL Query"))
        layout.addWidget(self.query_input)
        layout.addWidget(execute_query_button)
        layout.addWidget(self.query_result_display)

        widget.setLayout(layout)  # Yerleşimi widget'a uygula

        return widget

    def execute_query(self):
        # Sorguyu çalıştır
        query = self.query_input.toPlainText()
        if not query:
            QMessageBox.warning(self, "Input Error", "Please enter a query")
            return

        message, result = self.db.execute_query(query)
        QMessageBox.information(self, "Execute Query", message)

        if result:
            num_rows = len(result)
            if num_rows > 0:
                num_cols = len(result[0])
                self.query_result_display.setRowCount(num_rows)
                self.query_result_display.setColumnCount(num_cols)
                for i in range(num_rows):
                    for j in range(num_cols):
                        item = QTableWidgetItem(str(result[i][j]))
                        self.query_result_display.setItem(i, j, item)
            else:
                self.query_result_display.setRowCount(0)
                self.query_result_display.setColumnCount(0)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()  # Ana pencereyi oluştur
    window.show()  # Ana pencereyi göster

    sys.exit(app.exec_())  # Uygulamayı çalıştır