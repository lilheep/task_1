import models
import tkinter as tk
from tkinter import ttk, messagebox
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"

window = tk.Tk()
window.geometry('500x500')
window.resizable(False, False)

notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)


def create_table_page(notebook, table_model, page_title):

    frame = ttk.Frame(notebook)
    notebook.add(frame, text=page_title)

    tree = ttk.Treeview(frame, columns=("id", "user_name", "password"), show="headings")

    tree.heading("id", text="id")
    tree.heading("user_name", text="user_name")
    tree.heading("password", text="password")
    tree.column("id", width=50, anchor='center')
    tree.column("user_name", width=150, anchor='center')
    tree.column("password", width=200, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True)

    def load_data():
 
        tree.delete(*tree.get_children())
        for record in table_model.select():
            tree.insert('', 'end', values=(record.id, record.user_name, record.password))

    def add_record():
  
        def save_record():
            username = entry_name.get().strip()
            password = entry_password.get().strip()

            if username and password:
                try:
                    table_model.create(user_name=username, password=password)
                    load_data()
                    messagebox.showinfo('Success!', 'The record has been added')
                    add_window.destroy()

                except Exception as e:
                    messagebox.showerror('Error!', f'Failed to add record: {e}')
            else:
                messagebox.showwarning('Error!', 'Fill in all fields')

        add_window = tk.Toplevel(window)
        add_window.geometry('200x300')
        add_window.title('Add Record')

        tk.Label(add_window, text='Name:').pack(pady=5)
        entry_name = tk.Entry(add_window)
        entry_name.pack(pady=5)

        tk.Label(add_window, text='Password:').pack(pady=5)
        entry_password = tk.Entry(add_window)
        entry_password.pack(pady=5)

        tk.Button(add_window, text='Save', command=save_record).pack(pady=10)

    def edit_record():

        selected = tree.selection()
        if not selected:
            messagebox.showwarning('Attention!', 'Select a record to edit')
            return

        record_id = tree.item(selected[0])['values'][0]

        def save_edit():
            username = entry_name.get().strip()
            password = entry_password.get().strip()

            if username and password:
                try:
                    record = table_model.get(table_model.id == record_id)
                    record.user_name = username
                    record.password = password
                    record.save()
                    load_data()
                    messagebox.showinfo('Success!', 'Record has been updated!')
                    edit_window.destroy()

                except Exception as e:
                    messagebox.showerror('Error!', f"Couldn't update record: {e}")
            else:
                messagebox.showwarning('Attention!', 'All fields must be filled in!')

        record = table_model.get(table_model.id == record_id)

        edit_window = tk.Toplevel(window)
        edit_window.geometry('200x300')
        edit_window.title('Edit Record')

        tk.Label(edit_window, text='Name:').pack(pady=5)
        entry_name = tk.Entry(edit_window)
        entry_name.insert(0, record.user_name)
        entry_name.pack(pady=5)

        tk.Label(edit_window, text='Password:').pack(pady=5)
        entry_password = tk.Entry(edit_window)
        entry_password.insert(0, record.password)
        entry_password.pack(pady=5)

        tk.Button(edit_window, text='Save', command=save_edit).pack(pady=10)

    def delete_record():
 
        selected = tree.selection()
        if not selected:
            messagebox.showwarning('Attention!', 'Select a record to delete')
            return

        record_id = tree.item(selected[0])['values'][0]
        if messagebox.askyesno('Confirm Deletion', 'Are you sure you want to delete the selected record?'):
            try:
                record = table_model.get(table_model.id == record_id)
                record.delete_instance()
                load_data()
                messagebox.showinfo('Success!', 'Record has been deleted')
            except Exception as e:
                messagebox.showerror('Error!', f'Failed to delete record: {e}')

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text='Add', command=add_record).pack(side='left', padx=5)
    tk.Button(button_frame, text='Edit', command=edit_record).pack(side='left', padx=5)
    tk.Button(button_frame, text='Delete', command=delete_record).pack(side='left', padx=5)

    load_data()


models.db_connection.connect()

create_table_page(notebook, models.Users, "Users Table")
create_table_page(notebook, models.Staffs, "Staffs Table")
create_table_page(notebook, models.Students, "Students Table")

def close_connection():
    if not models.db_connection.is_closed():
        models.db_connection.close()
    window.destroy()

window.protocol('WM_DELETE_WINDOW', close_connection)

window.mainloop()
