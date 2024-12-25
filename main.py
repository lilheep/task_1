import models
import peewee
import tkinter as tk
from tkinter import ttk
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
    models.db.connect()
    for user in models.Users.select():
        tree.insert('', 'end', values=(user.id, user.user_name, user.password))
    
    models.db.close()

load_data()

window.mainloop()
