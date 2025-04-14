import os
from flask import Flask, render_template, request,jsonify
import sqlite3
import json, csv
import pandas as pd

class DBBrowserApp:
    def __init__(self, db_file_path=os.path.join(os.getcwd(), 'database'), 
                 db_file_name=None, 
                 csv_file_name = None, 
                 csv_file_path =os.path.join(os.getcwd(), 'csv'),
                 json_file_path = os.path.join(os.getcwd(), 'json'),
                 json_file_name = None,
                 scsv_file_path = os.path.join(os.getcwd(), 'savecsv'),
                 scsv_file_name = None,):
        
        self.app = Flask(__name__)
        self._db_file_path = db_file_path
        self._db_file_name = db_file_name
        self._db = None  # db açık mı değil mi kontrol etmek için
        self._csv_file_name = csv_file_name
        self._csv_file_path = csv_file_path
        self._json_file_path = json_file_path
        self._json_file_name = json_file_name
        self._scsv_file_path = scsv_file_path
        self._scsv_file_name = scsv_file_name
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/fileinfo', methods=['GET'])
        def get_file_info():
            return {'file_path': self._db_file_path}

        @self.app.route('/save', methods=['POST'])
        def save_file():
            data = request.get_json()
            self._db_file_path = data.get('file_path')
            self._db_file_name = data.get('file_name')
            
            if not self._db_file_name.endswith(".db"):
                self._db_file_name += ".db"

            if self._db_file_path and self._db_file_name:
                db_file_path = os.path.join(self._db_file_path, self._db_file_name)
                if not os.path.exists(self._db_file_path):
                    os.makedirs(self._db_file_path)
                # with open(db_file_path, 'w') as f:
                #     pass  # boş dosya oluşturulur
                conn = sqlite3.connect(db_file_path)
                
                cursor = conn.cursor()
                # Tabloları al
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables = cursor.fetchall()
                table_names = [table[0] for table in tables]
                    
                # Tablolara ait sütun adlarını ve türlerini al
                table_columns = {}
                for table_name in table_names:
                    cursor.execute(f"PRAGMA table_info({table_name});")
                    columns_info = cursor.fetchall()
                    columns = [{'name': col[1], 'type': col[2]} for col in columns_info]
                    table_columns[table_name] = columns
                    
                return {'message': 'File saved successfully','tables': table_names, 'table_columns': table_columns}, 201
            else:
                return {'error': 'File path or variable error'}, 400
            
        @self.app.route('/save-sql', methods=['POST']) # gerek yok gibi
        def save_sql():
            data = request.get_json()
            sql_query = data.get('sql')

            if self._db_file_name and sql_query:
                try:
                    cursor = self._db_file_name.cursor()
                    cursor.execute(sql_query)
                    self._db_file_name.commit()
                    return jsonify({'message': 'SQL executed and table created successfully'})
                except sqlite3.Error as e:
                    return jsonify({'error': str(e)}), 400
            else:
                return jsonify({'error': 'Invalid SQL query or database connection'}), 400
        
        
        @self.app.route('/create_table', methods=['POST']) #yeni tablo oluşturulduktan sonra fronta
        def create_table():
            data = request.get_json()
            sql_query = data.get('sql_query')
            db_file_path = os.path.join(self._db_file_path, self._db_file_name)
            if not sql_query:
                return {'error': 'SQL query is missing'}, 400
            
            try:
                with sqlite3.connect(db_file_path) as db:
                    cursor = db.cursor()
                    cursor.execute(sql_query)
                    db.commit()
                return {'message': 'Table created successfully'}, 201
            except sqlite3.Error as e:
                return {'error': str(e)}, 500
            
        @self.app.route('/close_database', methods=['POST'])
        def close_database():
            if self._db:  # Bağlantı kontrolü
                try:
                    self._db.close()
                    self._db = None
                    self._db_file_name = None
                    return jsonify({'message': 'Database successfully closed'}), 200
                except Exception as e:
                    return jsonify({'error': f'Error closing the database: {str(e)}'}), 500
            else:
                return jsonify({'error': 'No database connection to close'}), 400

                
        
        @self.app.route('/open_database', methods=['POST'])
        def open_database():
            try:
                self._db_file_name = request.json.get('file_name')
                if not self._db_file_name:
                    return jsonify({'error': 'No file name provided'}), 400
                if self._db_file_name.endswith('.db'):
                    conn = os.path.join(self._db_file_path, self._db_file_name)
                    self._db = sqlite3.connect(conn)  # Bağlantıyı self._db içine atayın
                    cursor = self._db.cursor()

                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    tables = cursor.fetchall()
                    table_names = [table[0] for table in tables]
                    
                    table_columns = {}
                    for table_name in table_names:
                        cursor.execute(f"PRAGMA table_info({table_name});")
                        columns_info = cursor.fetchall()
                        columns = [{'name': col[1], 'type': col[2]} for col in columns_info]
                        table_columns[table_name] = columns

                    return jsonify({'message': 'Database opened successfully', 'tables': table_names, 'table_columns': table_columns}), 200
                else:
                    return jsonify({'error': 'Invalid file format'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            
        @self.app.route('/execute_sql', methods=['POST'])
        def execute_sql():
            try:
                # Gelen JSON verisinden SQL sorgusunu alın
                sql_query = request.json.get('sql_query', '')

                # Eğer veritabanı bağlantısı yoksa veya SQL sorgusu yoksa hata döndür
                if not self._db or not sql_query:
                    return jsonify({'error': 'Invalid database connection or SQL query'}), 400
                
                conn = os.path.join(self._db_file_path, self._db_file_name)
                self._db = sqlite3.connect(conn) 
                # SQL sorgusunu veritabanında çalıştırın
                cursor = self._db.cursor()
                cursor.execute(sql_query)
                result = cursor.fetchall()

                # Sütun adlarını al
                column_names = [description[0] for description in cursor.description]

                # Sonucu JSON formatına dönüştürün
                result_data = {'column_names': column_names, 'result': result}

                # Sonucu JSON olarak yanıtlayın
                return jsonify({'data': result_data}), 200
            except sqlite3.Error as e:
                # Bir hata oluşursa, hata mesajını JSON olarak yanıtlayın
                return jsonify({'error': str(e)}), 500
            
        @self.app.route('/open_csv', methods=['POST'])
        def open_csv():
            try:
                data = request.get_json()
                self._csv_file_name = data.get('csvFile')
                print(f"csv_file_name: {self._csv_file_name}")
                print(f"csv_file_path: {self._csv_file_path}")
                print(f"db_file_path: {self._db_file_path}")
                print(f"db_file_name: {self._db_file_name}")
                csv_file_path = os.path.join(self._csv_file_path, self._csv_file_name)

                if not os.path.exists(csv_file_path):
                    return jsonify({'error': 'CSV file not found'}), 400

                df = pd.read_csv(csv_file_path)
                tables = df.values.tolist()
                column_names = df.columns.tolist()
                preview_data = {
                    'column_names': column_names,
                    'tables': tables,
                    'message': 'CSV file opened successfully'
                }

                return jsonify(preview_data), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        @self.app.route('/update_csv_preview', methods=['POST'])
        def update_csv_preview():
            try:
                data = request.get_json()
                self._csv_file_name = data.get('csvFile') 
                settings = data.get('settings')
                csv_file_path = os.path.join(self._csv_file_path, self._csv_file_name)

                if not os.path.exists(csv_file_path):
                    return jsonify({'error': 'CSV file not found'}), 400

                column_names_in_first_line = settings.get('columnNamesInFirstLine', True)
                field_separator = settings.get('fieldSeparator', ',')
                quote_character = settings.get('quoteCharacter', '"')
                encoding = settings.get('encoding', 'utf-8')
                trim_fields = settings.get('trimFields', False)

                df = pd.read_csv(
                    csv_file_path,
                    sep=field_separator,
                    quotechar=quote_character,
                    encoding=encoding,
                    skipinitialspace=trim_fields,
                    header=0 if column_names_in_first_line else None
                )

                tables = df.values.tolist()
                column_names = df.columns.tolist()

                preview_data = {
                    'column_names': column_names,
                    'tables': tables
                }

                return jsonify(preview_data), 200
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/add_csv_to_db', methods=['POST'])
        def add_csv_to_db():
            data = request.json
            table_name = data.get('table_name')
            
            csv_file_path = os.path.join(self._csv_file_path, self._csv_file_name)
            db_file_path = os.path.join(self._db_file_path, self._db_file_name)
            print(f"csv_file_path: {csv_file_path}")
            print(f"db_file_path: {db_file_path}")
            print(f"table_name: {table_name}")
            print(f"db dosya yolu: {self._db_file_path}")
            print(f"db dosya adı: {self._db_file_name}")
            print(f"csv dosya adı: {self._csv_file_name}")
            print(f"csv dosya yolu: {self._csv_file_path}")
            
            if not csv_file_path or not db_file_path or not table_name:
                return jsonify({"error": "Missing required parameters"}), 400

            # Check if CSV file exists
            if not os.path.exists(csv_file_path):
                return jsonify({"error": "CSV file not found"}), 404

            # Check if database file exists
            if not os.path.exists(db_file_path):
                return jsonify({"error": "Database file not found"}), 404

            try:
                # Read the CSV file into a DataFrame
                df = pd.read_csv(csv_file_path)

                # Connect to the SQLite database
                conn = sqlite3.connect(db_file_path)
                cursor = conn.cursor()

                # Create table if it doesn't exist
                df.to_sql(table_name, conn, if_exists='replace', index=False)

                conn.commit()

                return jsonify({"message": f"CSV data added to table '{table_name}' in database."}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/show_table', methods=['GET'])
        def show_table():
            try:
                print(f"db_file_path: {self._db_file_path}")
                print(f"db_file_name: {self._db_file_name}")
                if not self._db_file_name:
                    return jsonify({'error': 'No file name provided'}), 400
                if self._db_file_name.endswith('.db'):
                    # Dosya yolunu oluştur
                    db_file_path = os.path.join(self._db_file_path, self._db_file_name)
                    
                    # Veritabanını aç ve self._db'yi güncelle
                    self._db = sqlite3.connect(db_file_path)
                    cursor = self._db.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    table_names = cursor.fetchall()

                    tables_data = {}

                    for table in table_names:
                        table_name = table[0]
                        
                        # Get the structure of the table
                        cursor.execute("PRAGMA table_info({})".format(table_name))
                        table_structure = cursor.fetchall()
                        
                        # Get column names
                        columns = [column[1] for column in table_structure]
                        
                        # Query the data
                        cursor.execute('SELECT * FROM {}'.format(table_name))
                        data = cursor.fetchall()
                        
                        # Store data in a dictionary
                        tables_data[table_name] = {
                            'columns': columns,
                            'data': data
                        }

                    return jsonify({'message': 'Tables fetched successfully', 'tables': tables_data}), 200
                else:
                    return jsonify({'error': 'Invalid file format'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/get_table_names', methods=['GET'])
        def get_table_names():
            try:
                if not self._db_file_name:
                    return jsonify({'error': 'No file name provided'}), 400
                if self._db_file_name.endswith('.db'):
                    # Dosya yolunu oluştur
                    db_file_path = os.path.join(self._db_file_path, self._db_file_name)
                    
                    # Veritabanını aç ve self._db'yi güncelle
                    self._db = sqlite3.connect(db_file_path)
                    cursor = self._db.cursor()
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                    table_names = cursor.fetchall()
                    
                    # Extract table names from the fetched data
                    table_names = [table[0] for table in table_names]

                    return jsonify({'message': 'Table names fetched successfully', 'table_names': table_names}), 200
                else:
                    return jsonify({'error': 'Invalid file format'}), 400
            except Exception as e:
                return jsonify({'error': str(e)}), 500

        
        @self.app.route('/save_json', methods=['POST'])
        def save_json():
            try:
                # Frontend'den gelen tablo adlarını al
                selected_tables = request.json.get("selectedTables")

                # Veritabanı dosyasını aç
                db_file_path = os.path.join(self._db_file_path, self._db_file_name)
                self._db = sqlite3.connect(db_file_path)
                cursor = self._db.cursor()

                # Seçili tabloların verilerini al ve JSON dosyası oluştur
                for table_name in selected_tables:
                    cursor.execute(f"SELECT * FROM {table_name}")
                    data = cursor.fetchall()

                    # JSON dosyasını oluştur
                    if self._db_file_name.endswith(".db"):
                        self._json_file_name = f"{self._db_file_name[:-3]}.json"
                    else:
                        self._json_file_name = f"{self._db_file_name}.json"
                    json_file_path = os.path.join(self._json_file_path, self._json_file_name)

                    # Sütun adlarını al
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    columns_info = cursor.fetchall()
                    column_names = [col[1] for col in columns_info]

                    # JSON verisine sütun adlarını dahil et
                    json_data = {
                        "table_name": table_name,
                        "column_names": column_names,
                        "data": data
                    }
                    # JSON dosyasına yaz
                    with open(json_file_path, "w") as json_file:
                        json.dump(json_data, json_file)

                return jsonify({"message": "Data successfully saved as JSON files"}), 200

            except Exception as e:
                # Hata durumunda hatayı dön
                return jsonify({"error": str(e)}), 500
            
        @self.app.route('/save_csv', methods=['POST'])
        def save_csv():
            try:
                selected_tables = request.json.get("selectedTables")
                
                # Veritabanı dosyasını aç
                db_file_path = os.path.join(self._db_file_path, self._db_file_name)
                self._db = sqlite3.connect(db_file_path)
                cursor = self._db.cursor()

                # CSV dosyasını oluştur
                if self._db_file_name.endswith(".db"):
                    self._scsv_file_name = f"{self._db_file_name[:-3]}.csv"
                else:
                    self._scsv_file_name = f"{self._db_file_name}.csv"
                csv_file_path = os.path.join(self._scsv_file_path, self._scsv_file_name)

                # Seçili tabloların verilerini al ve CSV dosyasına dönüştür
                with open(csv_file_path, mode='w', newline='') as csv_file:
                    writer = csv.writer(csv_file)
                    for table_name in selected_tables:
                        # Tablo verilerini al
                        cursor.execute(f"SELECT * FROM {table_name}")
                        table_data = cursor.fetchall()
                        
                        # # Tablo başlığını yaz
                        # writer.writerow([f"Table: {table_name}"])
                        
                        # Tablo verilerini yaz
                        column_names = [description[0] for description in cursor.description]
                        writer.writerow(column_names)  # Sütun başlıklarını yaz

                        for row in table_data:
                            writer.writerow(row)

                return jsonify({"message": "Data successfully saved as CSV file"}), 200

            except Exception as e:
                # Hata durumunda hatayı dön
                return jsonify({"error": str(e)}), 500



    def run(self):
        self.app.run(debug=True)

if __name__ == '__main__':
    app = DBBrowserApp()
    app.run()