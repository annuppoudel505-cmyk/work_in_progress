
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create database and table
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # Insert default user
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password)
    VALUES (?, ?)
    """, ("admin", "1234"))

    conn.commit()
    conn.close()


# Login function
def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username = ? AND password = ?
    """, (username, password))

    user = cursor.fetchone()

    conn.close()

    if user:
        messagebox.showinfo("Success", f"Welcome {username}!")
        open_dashboard(username)
    else:
        messagebox.showerror("Error", "Invalid Username or Password")


# Dashboard window
def open_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.geometry("300x200")

    label = tk.Label(
        dashboard,
        text=f"Welcome {username}",
        font=("Arial", 16)
    )
    label.pack(pady=20)

    logout_btn = tk.Button(
        dashboard,
        text="Logout",
        command=dashboard.destroy
    )
    logout_btn.pack()


# Create database
create_database()


# Main window
root = tk.Tk()
root.title("Login Portal")
root.geometry("350x250")


title = tk.Label(root, text="Login Portal", font=("Arial", 18))
title.pack(pady=10)


# Username
username_label = tk.Label(root, text="Username")
username_label.pack()

username_entry = tk.Entry(root)
username_entry.pack()


# Password
password_label = tk.Label(root, text="Password")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()


# Login Button
login_button = tk.Button(
    root,
    text="Login",
    command=login
)
login_button.pack(pady=15)


root.mainloop()