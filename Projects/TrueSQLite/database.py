import sqlite3

def create_table():
    conn =sqlite3.connect('Data.db')
    cursor = conn.cursor() #for interact with database

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Data (
            id INTEGER PRIMARY KEY,
            name TEXT,
            desc TEXT,
            status TEXT, 
            email TEXT,
            gender TEXT,
            title TEXT,
            number INTEGER)''') #status via named type
    conn.commit()
    conn.close()

def fetch_data():
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Data')
    data = cursor.fetchall()
    conn.close()
    return data

def insert_data(id ,name, desc, status, email, gender, title, number):
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Data (id ,name, desc, status, email, gender, title, number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                    (id ,name, desc, status, email, gender, title, number))
    conn.commit()
    conn.close()

def delete_data(id):
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Data WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def update_data(new_name, new_desc, new_status, new_email, new_gender, new_title, new_number, id):
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Data SET name = ?, desc = ?, status = ?, email = ?, gender = ?, title = ?, number = ? WHERE id = ?",
                   (new_name, new_desc, new_status, new_email, new_gender, new_title, new_number, id))
    conn.commit()
    conn.close()

def id_exists(id):
    conn = sqlite3.connect('Data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Data WHERE id = ?', (id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0 #database ids matches or not matches

create_table()
