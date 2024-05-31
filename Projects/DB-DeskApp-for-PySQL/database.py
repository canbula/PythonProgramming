import firebase_admin
from firebase_admin import credentials, db
import pyrebase
import pandas as pd
from tabulate import tabulate


class Firebase:
    CREDENTIALS_FILE = "db.json"
    DATABASE_URL = "https://dbdeskapp-e4d13-default-rtdb.europe-west1.firebasedatabase.app/"
    API_KEY = "AIzaSyD-0p1f8b34D_dyke74CdobrQDcJCAfSsE"
    PROJECT_ID = "dbdeskapp-e4d13"

    def __init__(self):
        self.cred = credentials.Certificate(self.CREDENTIALS_FILE)
        firebase_admin.initialize_app(self.cred, {
            "databaseURL": self.DATABASE_URL
        })
        self.ref = db.reference("/")
        
        self.config = {
            "apiKey": self.API_KEY,
            "authDomain": f"{self.PROJECT_ID}.firebaseapp.com",
            "databaseURL": self.DATABASE_URL,
            "storageBucket": f"{self.PROJECT_ID}.appspot.com",
        }
        self.firebase = pyrebase.initialize_app(self.config)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

    def login(self, email, password):
        user = self.auth.sign_in_with_email_and_password(email, password)
        return user

    def register(self, email, password):
        user = self.auth.create_user_with_email_and_password(email, password)
        return user

    def get_user(self):
        return self.auth.current_user

    def create_new_database(self, database_name):
        user = self.get_user()
        if user:
            user_uid = user['localId']
            self.db.child("users").child(user_uid).child("databases").child(database_name).set({"name": database_name})
            return database_name
        else:
            print("User is not authenticated.")
            return None

    def create_table(self, user_id, database_name, table_name, table_id, table_info):
        try:
            table_ref = self.db.child("users").child(user_id).child("databases").child(database_name).child("tables").child(table_name)
            table_ref.child("table_id").set(table_id)
            table_ref.child("table_name").set(table_name)
            table_ref.child("info").set(table_info)
            print(f"Table '{table_name}' created successfully in database '{database_name}'.")
        except Exception as e:
            print(f"Error creating table: {e}")

    def create_column(self, user_id, selected_table_name, col_name, data_type, primary_key, foreign_key):
        try:
            # Debug print statements for tracking values
            print(f"User ID: {user_id}")
            print(f"Table Name: {selected_table_name}")
            print(f"Column Name: {col_name}, Data Type: {data_type}, Primary Key: {primary_key}, Foreign Key: {foreign_key}")

            columns_ref = self.db.child("user_tables").child(user_id).child(selected_table_name).child("columns").child(col_name)
            columns_ref.set({
                "column_name": col_name,
                "data_type": data_type,
                "primary_key": primary_key,
                "foreign_key": foreign_key
            })
            print(f"Column '{col_name}' created successfully in table '{selected_table_name}'.")
        except Exception as e:
            print(f"Error creating column: {e}")



            
    def get_user_databases(self, user_id):
        try:
            return self.db.child("users").child(user_id).get().val()
        except Exception as e:
            print(f"Error fetching user databases: {e}")
            return None

    def save_table_info(self, database_name, table_name, table_id):
        try:
            table_info = {"table_name": table_name, "table_id": table_id}
            user = self.get_user()
            if user:
                user_uid = user['localId']
                user_tables_ref = self.db.child("users").child(user_uid).child("databases").child(database_name).child("tables").child(table_name)
                user_tables_ref.set(table_info)
                print(f"Table '{table_name}' info saved successfully in database '{database_name}'.")
                return True
            else:
                print("User is not authenticated.")
                return False
        except Exception as e:
            print(f"Error saving table info: {e}")
            return False

    def get_table_names(self, database_name):
        try:
            table_names = []
            user = self.get_user()
            if user:
                user_uid = user['localId']
                tables_ref = self.db.child("users").child(user_uid).child("databases").child(database_name).child("tables")
                table_snapshots = tables_ref.get()
                if table_snapshots:
                    for table_snapshot in table_snapshots.each():
                        table_info = table_snapshot.val()
                        if "table_name" in table_info:
                            table_names.append(table_info["table_name"])
                        else:
                            print(f"Warning: 'table_name' key not found in table info: {table_info}")
                else:
                    print("No tables found for the selected database.")
            else:
                print("User is not authenticated.")
            print(f"Retrieved table names: {table_names}")  # Debugging line
            return table_names
        except Exception as e:
            print(f"Error getting table names: {e}")
            return []

    def get_database_names(self):
        user = self.get_user()
        if user:
            user_uid = user['localId']
            databases = self.db.child("users").child(user_uid).child("databases").get().val()
            return [db['name'] for db in databases.values()] if databases else []
        else:
            print("User is not authenticated.")
            return []

    def get_dbtable_names(self, database_name):
        try:
            user = self.get_user()
            if user:
                user_uid = user['localId']
                db_ref = self.db.child("users").child(user_uid).child("databases").child(database_name)
                db_info = db_ref.get().val()
                if db_info:
                    table_names = []
                    tables_ref = db_ref.child("tables")
                    tables = tables_ref.get()
                    if tables:
                        for table_name, _ in tables.items():
                            table_names.append(table_name)
                    return table_names
                else:
                    print("Database not found.")
                    return []
            else:
                print("User is not authenticated.")
                return []
        except Exception as e:
            print(f"Error getting table names: {e}")
            return []

    def get_columns(self, user_id, selected_table_name):
        try:
            print(f"Retrieving columns for user ID: {user_id}, table: {selected_table_name}")
            columns_ref = self.db.child("user_tables").child(user_id).child(selected_table_name).child("columns")
            columns = []
            column_snapshots = columns_ref.get()
            if column_snapshots.each() is not None:
                for column_snapshot in column_snapshots.each():
                    column_info = column_snapshot.val()
                    column_name = column_snapshot.key()  # column name is the key
                    column_info["name"] = column_name  # add the column name to the column info
                    columns.append(column_info)
                print(f"Columns retrieved: {columns}")
            else:
                print("No columns found.")
            return columns
        except Exception as e:
            print(f"Error getting columns: {e}")
            return []



        
    def add_data_to_table(self, user_id, database_name, table_name, data):
        try:
            table_ref = self.db.child("users").child(user_id).child("databases").child(database_name).child("tables").child(table_name).child("data")
            table_ref.push(data)
            print(f"Data added to table '{table_name}' in database '{database_name}'.")
        except Exception as e:
            print(f"Error adding data to table: {e}")

    def get_table_data(self, user_id, database_name, table_name):
        try:
            data_ref = self.db.child("users").child(user_id).child("databases").child(database_name).child("tables").child(table_name).child("data")
            data = data_ref.get().val()
            if data:
                df = pd.DataFrame(data.values())
                return df
            else:
                print(f"No data found in table '{table_name}'.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error getting table data: {e}")
            return pd.DataFrame()

    def display_table_data(self, user_id, database_name, table_name):
        df = self.get_table_data(user_id, database_name, table_name)
        if not df.empty:
            print(tabulate(df, headers='keys', tablefmt='psql'))
        else:
            print(f"No data to display for table '{table_name}'.")
            
    def delete_database(self, user_id, database_name):
        try:
            self.db.child("users").child(user_id).child("databases").child(database_name).remove()
            print(f"Database '{database_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting database: {e}")

    def delete_table(self, user_id, database_name, table_name):
        try:
            self.db.child("users").child(user_id).child("databases").child(database_name).child("tables").child(table_name).remove()
            print(f"Table '{table_name}' in database '{database_name}' deleted successfully.")
        except Exception as e:
            print(f"Error deleting table: {e}")

    
    def delete_column(self, user_id, database_name, table_name, column_name):
        try:
            # Delete column from user_tables
            self.db.child("user_tables").child(user_id).child(table_name).child("columns").child(column_name).remove()
            print(f"Column '{column_name}' in table '{table_name}' deleted successfully from user_tables.")

            # Delete column from users
            user_ref = self.db.child("users").child(user_id).child("databases").child(database_name).child("tables")
            tables = user_ref.get()

            if tables.each() is not None:
                for table_snapshot in tables.each():
                    table_data = table_snapshot.val()
                    if table_data.get("table_name") == table_name:
                        data_snapshots = table_data.get("data", {})
                        for data_id, data in data_snapshots.items():
                            if isinstance(data, dict) and column_name in data:
                                self.db.child("users").child(user_id).child("databases").child(database_name).child("tables").child(table_snapshot.key()).child("data").child(data_id).child(column_name).remove()
                        print(f"Column '{column_name}' in table '{table_name}' deleted successfully from users data.")
        except Exception as e:
            print(f"Error deleting column: {e}")
            

