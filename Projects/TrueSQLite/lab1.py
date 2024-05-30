import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox, filedialog
import database
import csv

app = customtkinter.CTk()
app.title('Database Management System')
app.geometry('1300x760')
app.config(bg='#161C25')
app.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')


def add_to_treeview():
    data = database.fetch_data()
    print("Fetched Data for TreeView:", data)  # Debugging print to check fetched data
    tree.delete(*tree.get_children())
    for item in data:
        tree.insert('', END, values=item)
    print("TreeView updated.")


def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
        tree.focus('')
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    desc_entry.delete(0, END)
    variable1.set('Male')
    variable2.set('Select')
    status_entry.delete(0, END)
    email_entry.delete(0, END)
    title_entry.delete(0, END)
    number_entry.delete(0, END)


def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        desc_entry.insert(0, row[2])
        variable2.set(row[3])
        email_entry.insert(0, row[4])
        variable1.set(row[5])
        title_entry.insert(0, row[6])
        number_entry.insert(0, row[7])
    else:
        pass


def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a data to delete.')
    else:
        id = id_entry.get()
        database.delete_data(id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been deleted.')


def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose a Data to update.')
    else:
        id = id_entry.get()
        name = name_entry.get()
        desc = desc_entry.get()
        status = variable2.get()
        email = email_entry.get()
        gender = variable1.get()
        title = title_entry.get()
        number = number_entry.get()

        # Ensure that all fields are not empty
        if not (id and name and desc and status and email and gender and title and number):
            messagebox.showerror('Error', 'Enter all fields.')
            return

        # Debug prints to check values
        print(f"Updating data with ID: {id}")
        print(f"Name: {name}")
        print(f"Description: {desc}")
        print(f"Status: {status}")
        print(f"Email: {email}")
        print(f"Gender: {gender}")
        print(f"Title: {title}")
        print(f"Number: {number}")

        # Ensure that the update function is called
        database.update_data(name, desc, status, email, gender, title, number, id)

        # Fetch and print data directly from the database after update
        updated_data = database.fetch_data()
        print("Data after update:", updated_data)

        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been updated.')


def insert():
    id = id_entry.get()
    name = name_entry.get()
    desc = desc_entry.get()
    status = variable2.get()
    email = email_entry.get()
    gender = variable1.get()
    title = title_entry.get()
    number = number_entry.get()
    if not (id and name and desc and status and email and gender and title and number):
        messagebox.showerror('Error', 'Enter all fields.')
    elif database.id_exists(id):
        messagebox.showerror('Error', 'ID already exists.')
    else:
        database.insert_data(id, name, desc, status, email, gender, title, number)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been inserted.')


def export_to_csv():
    data = database.fetch_data()
    if not data:
        messagebox.showinfo('No Data', 'There is no data to export.')
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Name', 'Description', 'Type', 'Email', 'Gender', 'Title', 'Number'])
        writer.writerows(data)

    messagebox.showinfo('Success', 'Data has been exported to CSV file successfully.')


def import_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip header row
        for row in reader:
            if not database.id_exists(row[0]):
                database.insert_data(*row)

    add_to_treeview()
    messagebox.showinfo('Success', 'Data has been imported from CSV file successfully.')


id_label = customtkinter.CTkLabel(app, font=font1, text='ID:', text_color='#fff', bg_color='#161C25')
id_label.place(x=20, y=20)

id_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                  border_width=2, width=180)
id_entry.place(x=100, y=20)

name_label = customtkinter.CTkLabel(app, font=font1, text='Name:', text_color='#fff', bg_color='#161C25')
name_label.place(x=20, y=80)

name_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                    border_width=2, width=180)
name_entry.place(x=100, y=80)

desc_label = customtkinter.CTkLabel(app, font=font1, text='Desc:', text_color='#fff', bg_color='#161C25')
desc_label.place(x=20, y=140)

desc_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                    border_width=2, width=180)
desc_entry.place(x=100, y=140)

status_label = customtkinter.CTkLabel(app, font=font1, text='Status:', text_color='#fff', bg_color='#161C25')
status_label.place(x=20, y=200)

status_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                      border_width=2, width=180)
status_entry.place(x=100, y=200)

email_label = customtkinter.CTkLabel(app, font=font1, text='Email:', text_color='#fff', bg_color='#161C25')
email_label.place(x=20, y=260)

email_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                     border_width=2, width=180)
email_entry.place(x=100, y=260)

gender_label = customtkinter.CTkLabel(app, font=font1, text='Gender:', text_color='#fff', bg_color='#161C25')
gender_label.place(x=20, y=320)

gender_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                      border_width=2, width=180)
gender_entry.place(x=100, y=320)

title_label = customtkinter.CTkLabel(app, font=font1, text='Title:', text_color='#fff', bg_color='#161C25')
title_label.place(x=20, y=380)

title_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                     border_width=2, width=180)
title_entry.place(x=100, y=380)

number_label = customtkinter.CTkLabel(app, font=font1, text='Number:', text_color='#fff', bg_color='#161C25')
number_label.place(x=20, y=440)

number_entry = customtkinter.CTkEntry(app, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                      border_width=2, width=180)
number_entry.place(x=100, y=440)

options = ['Male', 'Female', 'Other']
optionss = ['Select', 'Option1', 'Option2']

variable1 = StringVar(app)
variable2 = StringVar(app)

gender_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff',
                                           dropdown_hover_color='#0C9295', button_color='#0C9295',
                                           button_hover_color='#0C9295', border_color='#0C9295', width=180,
                                           variable=variable1, values=options, state='readonly')
gender_options.set('Male')
gender_options.place(x=100, y=320)

status_options = customtkinter.CTkComboBox(app, font=font1, text_color='#000', fg_color='#fff',
                                           dropdown_hover_color='#0C9295', button_color='#0C9295',
                                           button_hover_color='#0C9295', border_color='#0C9295', width=180,
                                           variable=variable2, values=optionss, state='readonly')
status_options.set('Select')
status_options.place(x=100, y=200)

add_button = customtkinter.CTkButton(app, command=insert, font=font1, text_color='#fff', text='Add Data',
                                     fg_color='#05A312', hover_color='#00850B', bg_color='#161C25', cursor='hand2',
                                     corner_radius=15, width=260)
add_button.place(x=20, y=500)

clear_button = customtkinter.CTkButton(app, command=lambda: clear(True), font=font1, text_color='#fff', text='New Data',
                                       fg_color='#161C25', hover_color='#FF5002', bg_color='#161C25',
                                       border_color='#F15704', border_width=2, cursor='hand2', corner_radius=15,
                                       width=260)
clear_button.place(x=20, y=540)

update_button = customtkinter.CTkButton(app, command=update, font=font1, text_color='#fff', text='Update Data',
                                        fg_color='#161C25', hover_color='#FF5002', bg_color='#161C25',
                                        border_color='#F15704', border_width=2, cursor='hand2', corner_radius=15,
                                        width=260)
update_button.place(x=20, y=580)

delete_button = customtkinter.CTkButton(app, command=delete, font=font1, text_color='#fff', text='Delete Data',
                                        fg_color='#E40404', hover_color='#AE0000', bg_color='#161C25',
                                        border_color='#E40404', border_width=2, cursor='hand2', corner_radius=15,
                                        width=260)
delete_button.place(x=20, y=620)

export_button = customtkinter.CTkButton(app, command=export_to_csv, font=font1, text_color='#fff', text='Export to CSV',
                                        fg_color='#0C9295', hover_color='#087A6B', bg_color='#161C25', cursor='hand2',
                                        corner_radius=15, width=260)
export_button.place(x=20, y=660)

import_button = customtkinter.CTkButton(app, command=import_from_csv, font=font1, text_color='#fff',
                                        text='Import from CSV', fg_color='#0C9295', hover_color='#087A6B',
                                        bg_color='#161C25', cursor='hand2', corner_radius=15, width=260)
import_button.place(x=20, y=700)

style = ttk.Style(app)

style.theme_use('clam')
style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
style.map('Treeview', background=[('selected', '#1A8F2D')])

tree = ttk.Treeview(app, height=30)

tree['columns'] = ('ID', 'Name', 'Description', 'Type', 'Email', 'Gender', 'Title', 'Number')

tree.column('#0', width=0, stretch=tk.NO)  # hide first default column
tree.column('ID', anchor=tk.CENTER, width=120)
tree.column('Name', anchor=tk.CENTER, width=120)
tree.column('Description', anchor=tk.CENTER, width=120)
tree.column('Type', anchor=tk.CENTER, width=120)
tree.column('Email', anchor=tk.CENTER, width=120)
tree.column('Gender', anchor=tk.CENTER, width=120)
tree.column('Title', anchor=tk.CENTER, width=120)
tree.column('Number', anchor=tk.CENTER, width=120)

tree.heading('ID', text='ID')
tree.heading('Name', text='Name')
tree.heading('Description', text='Description')
tree.heading('Type', text='Type')
tree.heading('Email', text='Email')
tree.heading('Gender', text='Gender')
tree.heading('Title', text='Title')
tree.heading('Number', text='Number')

tree.place(x=300, y=20)

tree.bind('<ButtonRelease-1>', display_data)

add_to_treeview()

app.mainloop()
