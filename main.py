import models
import tkinter as tk
from tkinter import ttk, messagebox
import os

os.environ['TCL_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\User\AppData\Local\Programs\Python\Python313\tcl\tk8.6"

window = tk.Tk()
window.geometry('500x500')
frame = tk.Frame(width=500, height=500)
window.resizable(False, False)
frame.pack()

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
    for user in models.Users.select():
        tree.insert('', 'end', values=(user.id, user.user_name, user.password))

def add_user():
    def save_user():
        username = entry_name.get().strip()
        password = entry_password.get().strip()
    
        if username and password:
            try:
                
                models.Users.create(user_name=username, password=password)
                load_data()
                messagebox.showinfo('Success!', 'The user has been added')
                add_window.destroy()
                
            except Exception as e:
                messagebox.showerror('Error!', f'It is impossible to add a user: {e}')
                
        else:
            messagebox.showwarning('Error!', 'Fill in all the fields')
            
    add_window = tk.Toplevel(window)
    add_window.geometry('200x300')
    add_window.title('Add user')
        
    tk.Label(add_window, text='Name user:').pack(pady=5)
    entry_name = tk.Entry(add_window)
    entry_name.pack(pady=5)
        
    tk.Label(add_window, text='Password:').pack(pady=5)
    entry_password = tk.Entry(add_window)
    entry_password.pack(pady=5)
        
    tk.Button(add_window, text='Save', command=save_user).pack(pady=10)

def edit_user():
    
    seleced = tree.selection()
    if not seleced:
        messagebox.showwarning('Attention!', 'Select a user for edit')
        return
    
    user_id = tree.item(seleced[0])['values'][0]
    def save_edit():
        
        username = entry_name.get().strip()
        password = entry_password.get().strip()

        if username and password:
            try:
    
                user = models.Users.get(models.Users.id == user_id)
                user.user_name = username
                user.password = password
                user.save()
                load_data()
                messagebox.showinfo('Success!', "The user's data has been updated!")
                edit_window.destroy()
            
            except Exception as e:
                messagebox.showerror('Error!', f"Couldn't update user data: {e}")
        
        else:
            messagebox.showwarning('Attention!', 'All fields must be filled in!')
        
    user = models.Users.get(models.Users.id == user_id)
         
    edit_window = tk.Toplevel(window)
    edit_window.geometry('200x300')
    edit_window.title('Edit user')
        
    tk.Label(edit_window, text='Name user:').pack(pady=5)
    entry_name = tk.Entry(edit_window)
    entry_name.insert(0, user.user_name)
    entry_name.pack(pady=5)
        
    tk.Label(edit_window, text='Password:').pack(pady=5)
    entry_password = tk.Entry(edit_window)
    entry_password.insert(0, user.password)
    entry_password.pack(pady=5) 
        
    tk.Button(edit_window, text='Save', command=save_edit).pack(pady=10) 
        
def delete_user():
    selected = tree.selection()
    
    if not selected:
        messagebox.showwarning('Attetion!', 'Select the user to delete') 
        return
    user_id = tree.item(selected[0])['values'][0]
    if messagebox.askyesno('Confirm the deletion!', 'Are you sure you want to delete the selected user?'):
        try:
            
            user = models.Users.get(models.Users.id == user_id)
            user.delete_instance() 
            load_data()
            messagebox.showinfo('Success!', 'The selected user has been deleted')   
        except Exception as e:
            messagebox.showerror('Error!', f'The user has not been deleted: {e}') 
        
button_frame = tk.Frame(window)
button_frame.pack(pady=10)

tk.Button(button_frame, text='Add user', command=add_user).pack(side='left', padx=5)
tk.Button(button_frame, text='Edit user', command=edit_user).pack(side='left', padx=5)
tk.Button(button_frame, text='Delete user', command=delete_user).pack(side='left', padx=5)


models.db_connection.connect()

load_data()

def close_connection():
    if not models.db_connection.is_closed():
        models.db_connection.close()
    window.destroy()

window.protocol('WM_DELETE_WINDOW', close_connection)

window.mainloop()