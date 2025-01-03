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

columns = {models.Users: ('id', 'user_name', 'password'),
           models.Staffs: ('id', 'staff_name', 'staff_password'),
            models.Students: ('id', 'student_name', 'student_password')}


def create_table_page(notebook, table_model, page_title):

    frame = ttk.Frame(notebook)
    notebook.add(frame, text=page_title)
    
    table_columns = columns[table_model]

    tree = ttk.Treeview(frame, columns=table_columns, show="headings")
    
    for col in table_columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    tree.pack(fill=tk.BOTH, expand=True)

    def load_data():
 
        tree.delete(*tree.get_children())
        for record in table_model.select():
            tree.insert('', 'end', values=tuple(getattr(record, col) for col in table_columns))

    def add_record():
  
        def save_record():
            
            data = {col: entries[i].get().strip() for i, col in enumerate(table_columns[1:])}
            
            for i, col in enumerate(table_columns[1:], start=1):
                data[col] = entries[i-1].get().strip()
                
            if all(data.values()):
                
                try:
                    table_model.create(**data)
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
        
        entries = []
        
        for col in table_columns[1:]:
            tk.Label(add_window, text=f'{col.capitalize()}:').pack(pady=5)
            entry = tk.Entry(add_window)
            entry.pack(pady=5)
            entries.append(entry)

        tk.Button(add_window, text='Save', command=save_record).pack(pady=10)

    def edit_record():

        selected = tree.selection()
        if not selected:
            messagebox.showwarning('Attention!', 'Select a record to edit')
            return

        record_id = tree.item(selected[0])['values'][0]
        record = table_model.get(table_model.id == record_id)

        def save_edit():
            
            data = {col: entries[i].get().strip() for i, col in enumerate(table_columns[1:])}
                
            if all(data.values()):
                try:
                    for col, value in data.items():
                        setattr(record, col, value)
                    record.save()
                    load_data()
                    messagebox.showinfo('Success!', 'Record has been updated!')
                    edit_window.destroy()
                
                except Exception as e:
                    messagebox.showerror('Error!', f"Couldn't update record: {e}")
            
            else:
                messagebox.showwarning('Attention!', 'All fields must be filled in!')

        edit_window = tk.Toplevel(window)
        edit_window.geometry('200x300')
        edit_window.title('Edit Record')

        entries = []
        
        for col in table_columns[1:]:
            tk.Label(edit_window, text=f'{col.capitalize()}:').pack(pady=5)
            entry = tk.Entry(edit_window)
            entry.insert(0, getattr(record, col))
            entry.pack(pady=5)
            entries.append(entry)

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
