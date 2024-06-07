from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Flash mesajları için gerekli

def get_db_connection():
 
    conn = sqlite3.connect('x4sqlite1.db')
    conn.row_factory = sqlite3.Row
    return conn
        

@app.route('/')
def index():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    conn.close()
    return render_template('index.html', tables=[table['name'] for table in tables])

@app.route('/table/<table_name>')
def select_table(table_name):
    conn = get_db_connection()
    data = conn.execute(f'SELECT *, rowid as id FROM {table_name}').fetchall()  # rowid as id eklendi
    columns = [column[1] for column in conn.execute(f'PRAGMA table_info({table_name})').fetchall()]
    columns.append('id')  # id sütununu ekle
    conn.close()
    return render_template('table.html', table_name=table_name, data=data, columns=columns)

@app.route('/table/<table_name>/add', methods=['GET', 'POST'])
def add_data(table_name):
    conn = get_db_connection()
    columns = [column[1] for column in conn.execute(f'PRAGMA table_info({table_name})').fetchall()]
    if request.method == 'POST':
        values = [request.form.get(column) for column in columns]
        placeholders = ', '.join(['?'] * len(columns))
        
        try:
            conn.execute(f'INSERT INTO {table_name} ({", ".join(columns)}) VALUES ({placeholders})', values)
            conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                conn.close()
                flash("Error: This operation cannot be completed because it violates a unique constraint.", "error")
                return redirect(url_for('select_table', table_name=table_name))
            else:
                raise
        conn.close()
        return redirect(url_for('select_table', table_name=table_name))
    conn.close()
    return render_template('add_data.html', table_name=table_name, columns=columns)

@app.route('/table/<table_name>/delete/<int:id>', methods=['POST'])
def delete_data(table_name, id):
    conn = get_db_connection()
    conn.execute(f'DELETE FROM {table_name} WHERE rowid = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('select_table', table_name=table_name))

@app.route('/table/<table_name>/update/<int:id>', methods=['GET', 'POST'])
def update_data(table_name, id):
    conn = get_db_connection()
    columns = [column[1] for column in conn.execute(f'PRAGMA table_info({table_name})').fetchall()]
    if request.method == 'POST':
        values = [request.form.get(column) for column in columns]
        set_clause = ', '.join([f'{column} = ?' for column in columns])
        values.append(id)
        
        try:
            conn.execute(f'UPDATE {table_name} SET {set_clause} WHERE rowid = ?', values)
            conn.commit()
        except sqlite3.IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                conn.close()
                flash("Error: This operation cannot be completed because it violates a unique constraint.", "error")
                return redirect(url_for('select_table', table_name=table_name))
            else:
                raise
        
        conn.close()
        return redirect(url_for('select_table', table_name=table_name))
    
    row = conn.execute(f'SELECT *, rowid as id FROM {table_name} WHERE rowid = ?', (id,)).fetchone()  # rowid as id eklendi
    conn.close()
    return render_template('update_data.html', table_name=table_name, columns=columns, row=row)

@app.route('/create_table', methods=['GET', 'POST'])
def create_table():
    if request.method == 'POST':
        table_name = request.form['table_name']
        columns = request.form['columns']
        conn = get_db_connection()
        try:
            conn.execute(f'CREATE TABLE {table_name} ({columns})')
            conn.commit()
            flash("Table created successfully.", "success")
        except sqlite3.Error as e:
            flash(f"Error creating table: {e}", "error")
        finally:
            conn.close()
        return redirect(url_for('index'))
    return render_template('create_table.html')

@app.route('/delete_table/<table_name>', methods=['POST'])
def delete_table(table_name):
    conn = get_db_connection()
    try:
        conn.execute(f'DROP TABLE {table_name}')
        conn.commit()
        flash("Table deleted successfully.", "success")
    except sqlite3.Error as e:
        flash(f"Error deleting table: {e}", "error")
    finally:
        conn.close()
    return redirect(url_for('index'))

@app.route('/query', methods=['GET', 'POST'])
def query():
    if request.method == 'POST':
        query = request.form['query']
        conn = get_db_connection()
        try:
            result = conn.execute(query).fetchall()
            columns = result[0].keys() if result else []
            conn.commit()
            flash("Query executed successfully.", "success")
        except sqlite3.Error as e:
            flash(f"Error executing query: {e}", "error")
            result = []
            columns = []
        finally:
            conn.close()
        return render_template('query.html', query=query, result=result, columns=columns)
    return render_template('query.html', query='', result=[], columns=[])

if __name__ == '__main__':
    app.run(debug=True)