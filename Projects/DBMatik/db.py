import sqlite3
import csv
import json

class Database:
    def __init__(self, db_name="database.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def create_database(self, name_user_gave):
        # Ensure the database name has a .db extension
        if not name_user_gave.endswith('.db'):
            name_user_gave += '.db'
            
        try:
            self.conn = sqlite3.connect(name_user_gave)
            self.cursor = self.conn.cursor()
            print("Connection and cursor set successfully")
        except sqlite3.Error as e:
            self.handle_error(e)

    def export_table_to_json(self, table_name, file_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]

            # Create a list of dictionaries where each dictionary represents a row
            data = [dict(zip(column_names, row)) for row in rows]

            with open(file_name, 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Data exported to {file_name} successfully.")
        except sqlite3.Error as e:
            self.handle_error(e)

    def create_table(self, table_name, columns, primary_key=None):
        try:
            columns_def = ', '.join([f"{col_name} {col_type}" for col_name, col_type in columns])
            if primary_key:
                columns_def += f", PRIMARY KEY ({primary_key})"
            create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"
            self.cursor.execute(create_table_sql)
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)


    def delete_table(self , table_name):
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_query(query)


    def insert_data(self, data_column: str, data, table_name):
        try:
            self.cursor.execute(f"INSERT INTO {table_name} ({data_column}) VALUES (?)", (data,))
        except sqlite3.Error as e:
            self.handle_error(e)

    def insert_all_data(self, data_list, table_name):
        try:
            if not data_list:
                return

            columns = data_list[0].keys()
            placeholders = ', '.join(['?'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            data_values = [tuple(row.values()) for row in data_list]

            self.cursor.executemany(query, data_values)
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)

    def execute_query(self, query, params=None):
        print("------")
        print("------")
        print("------")
        print("1")
        
        if self.cursor is None:
            raise Exception("Database connection is not established")
        print(f"Executing query: {query}")  # Debug statement
        print("2")
        self.cursor.execute(query, params or [])
        print("3")
        column_names = [desc[0] for desc in self.cursor.description] if self.cursor.description else []
        print("4")
        result = self.cursor.fetchall()
        print("5")
        print(f"Query executed: {query}")  # Debug statement
        print("6")
        return column_names, result


    def get_columns_of_table(self, table_name):
        try:
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            column_names = [col[1] for col in columns]
            
            return column_names
        except sqlite3.Error as e:
            self.handle_error(e)
            return []


    def update_data(self, table_name, data_list, unique_column):
        print("---------")
        print("---------")
        print("---------")
        
        i = 0
        try:
            if not data_list:
                return

            for row in data_list:
                columns = row.keys()
                print(columns)
                print(unique_column[i])
                set_clause = ', '.join([f"{col} = ?" if row[col] is not None else f"{col} = NULL" for col in columns if col != unique_column[i]])
                print(set_clause)
                query = f"UPDATE {table_name} SET {set_clause} WHERE {unique_column[i]} = ?"
                print(query)
                values = [row[col] for col in columns if col != unique_column[i]]
                print(values)
                unique_column_value = row.get(unique_column[i], None)
                print(unique_column_value)
                values.append(unique_column_value)
                print(values)
                self.cursor.execute(query, values)

            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)




    def delete_data(self, table, delete_conditions):
        try:
            if not delete_conditions:
                raise ValueError("Please enter at least one condition to delete")
            
            where_clause = ' AND '.join([f'{column} = ?' for column in delete_conditions.keys()])
            query = f'DELETE FROM {table} WHERE {where_clause}'
            values = list(delete_conditions.values())
            
            self.execute_query(query, values)
            self.conn.commit()
        except sqlite3.Error as e:
            self.handle_error(e)


    def get_tables(self):
        try:
            print("2")
            self.cursor.execute("SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;")
            tables = self.cursor.fetchall()
            
            return [table[0] for table in tables]
        except sqlite3.Error as e:
            self.handle_error(e)
            return []  # Return an empty list if there's an error
    
    def handle_error(self, error):
        print(f"An error occurred: {error}")

    def close_connection(self):
        if self.conn:
            self.conn.close()

    def export_table_to_text(self, table_name, file_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)
            
            print(f"Data exported to {file_name} successfully.")
        except sqlite3.Error as e:
            self.handle_error(e)

    def import_table_from_text(self, table_name, file_name):
        try:
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                columns = next(reader)
                data = [tuple(row) for row in reader]
                
            placeholders = ', '.join(['?'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            self.cursor.executemany(query, data)
            self.conn.commit()
            
            print(f"Data imported from {file_name} successfully.")
        except sqlite3.Error as e:
            self.handle_error(e)

    def export_table_to_csv(self, table_name, file_name):
        try:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            rows = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            
            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column_names)
                writer.writerows(rows)
            
            print(f"Data exported to {file_name} successfully.")
        except sqlite3.Error as e:
            self.handle_error(e)

    def import_table_from_csv(self, table_name, file_name):
        try:
            with open(file_name, 'r') as file:
                reader = csv.reader(file)
                columns = next(reader)
                data = [tuple(row) for row in reader]
                
            placeholders = ', '.join(['?'] * len(columns))
            query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
            
            self.cursor.executemany(query, data)
            self.conn.commit()
            
            print(f"Data imported from {file_name} successfully.")
        except sqlite3.Error as e:
            self.handle_error(e)




if __name__ == "__main__":
    deneme_db2 = Database()
    deneme_db2.create_database("deneme2.db")

    columns = [("User_id", "INTEGER"), ("User_name", "TEXT"), ("User_age", "INTEGER")]
    deneme_db2.create_table("Users1", columns, "User_id")

    data_list = [
        {"User_id": 3, "User_name": "Metehan Efe", "User_age": 23},
        {"User_id": 4, "User_name": "Barış Bağçeci", "User_age": 21},
        {"User_id": 5, "User_name": "Kubilay Çakmak", "User_age": 25}
    ]
    deneme_db2.insert_all_data(data_list, "Users1")

    query = "SELECT * FROM Users1"
    ##print(deneme_db2.execute_query(query))

    # Exporting data to CSV
    deneme_db2.export_table_to_csv("Users1", "users1_export.csv")

    # Importing data from CSV
    deneme_db2.create_table("Users2", columns, "User_id")
    deneme_db2.import_table_from_csv("Users2", "users1_export.csv")
    query = "SELECT * FROM Users2"
    deneme_db2.execute_query(query)

