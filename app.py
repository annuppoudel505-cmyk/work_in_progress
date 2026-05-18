import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
# ================= SIGNUP =================

def signup():
    username = signup_username.get()
    password = signup_password.get()
    confirm = signup_confirm.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match")
        return

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    try:
        cursor.execute("""
        INSERT INTO users (username, password, role)
        VALUES (?, ?, ?)
        """, (username, password, "user"))

        conn.commit()
        messagebox.showinfo(
            "Success",
            "Account created successfully!"
        )

        signup_window.destroy()

    except sqlite3.IntegrityError:
        messagebox.showerror(
            "Error",
            "Username already exists"
        )

    conn.close()


# ================= LOGIN =================

def login():
    username = username_entry.get()
    password = password_entry.get()

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username, role
    FROM users
    WHERE username=? AND password=?
    """, (username, password))

    user = cursor.fetchone()
    conn.close()

    if user:
        username, role = user

        messagebox.showinfo(
            "Success",
            f"Welcome {username}!"
        )

        if role == "super_admin":
            open_super_admin_dashboard(username)

        elif role == "admin":
            open_admin_dashboard(username)

        else:
            open_user_dashboard(username)

    else:
        messagebox.showerror(
            "Error",
            "Invalid username or password"
        )


# ================= SIGNUP PAGE =================

def open_signup():
    global signup_window
    global signup_username
    global signup_password
    global signup_confirm

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")
    signup_window.geometry("350x350")
    signup_window.config(bg="#f0f0f0")

    tk.Label(
        signup_window,
        text="Create Account",
        font=("Arial", 18, "bold"),
        bg="#f0f0f0"
    ).pack(pady=15)

    tk.Label(
        signup_window,
        text="Username",
        bg="#f0f0f0"
    ).pack()

    signup_username = tk.Entry(signup_window, width=30)
    signup_username.pack(pady=5)

    tk.Label(
        signup_window,
        text="Password",
        bg="#f0f0f0"
    ).pack()

    signup_password = tk.Entry(
        signup_window,
        show="*",
        width=30
    )
    signup_password.pack(pady=5)

    tk.Label(
        signup_window,
        text="Confirm Password",
        bg="#f0f0f0"
    ).pack()

    signup_confirm = tk.Entry(
        signup_window,
        show="*",
        width=30
    )
    signup_confirm.pack(pady=5)

    tk.Button(
        signup_window,
        text="Create Account",
        bg="green",
        fg="black",
        width=20,
        command=signup
    ).pack(pady=15)


# ================= USER DASHBOARD =================

def request_admin(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET admin_request = 1
    WHERE username = ?
    """, (username,))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        "Admin request sent!"
    )


def open_user_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("User Dashboard")
    dashboard.geometry("350x250")

    tk.Label(
        dashboard,
        text=f"Welcome {username}",
        font=("Arial", 16)
    ).pack(pady=20)

    tk.Label(
        dashboard,
        text="Role: Regular User"
    ).pack()

    tk.Button(
        dashboard,
        text="Request Admin Access",
        bg="orange",
        command=lambda:
        request_admin(username)
    ).pack(pady=10)

    tk.Button(
        dashboard,
        text="Logout",
        bg="red",
        fg="white",
        command=dashboard.destroy
    ).pack(pady=10)


# ================= ADMIN DASHBOARD =================

def open_admin_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("Admin Dashboard")
    dashboard.geometry("350x250")

    tk.Label(
        dashboard,
        text=f"Welcome Admin {username}",
        font=("Arial", 16)
    ).pack(pady=20)

    tk.Label(
        dashboard,
        text="Role: Admin"
    ).pack()

    tk.Button(
        dashboard,
        text="Logout",
        bg="red",
        fg="white",
        command=dashboard.destroy
    ).pack(pady=20)


# ================= SUPER ADMIN =================

def refresh_requests(tree):
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT username
    FROM users
    WHERE admin_request = 1
    AND role = 'user'
    """)

    users = cursor.fetchall()
    conn.close()

    for user in users:
        tree.insert("", tk.END, values=user)


def approve_admin(tree):
    selected = tree.focus()

    if not selected:
        messagebox.showerror(
            "Error",
            "Select a user"
        )
        return

    username = tree.item(selected)["values"][0]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE users
    SET role='admin',
        admin_request=0
    WHERE username=?
    """, (username,))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Success",
        f"{username} promoted to Admin"
    )

    refresh_requests(tree)


def open_super_admin_dashboard(username):
    dashboard = tk.Toplevel(root)
    dashboard.title("Super Admin Dashboard")
    dashboard.geometry("500x400")

    tk.Label(
        dashboard,
        text=f"Welcome {username}",
        font=("Arial", 18, "bold")
    ).pack(pady=10)

    tk.Label(
        dashboard,
        text="Pending Admin Requests"
    ).pack()

    tree = ttk.Treeview(
        dashboard,
        columns=("Username",),
        show="headings"
    )

    tree.heading(
        "Username",
        text="Username"
    )

    tree.pack(
        pady=10,
        fill="both",
        expand=True
    )

    refresh_requests(tree)

    tk.Button(
        dashboard,
        text="Approve as Admin",
        bg="green",
        fg="black",
        command=lambda:
        approve_admin(tree)
    ).pack(pady=5)

    tk.Button(
        dashboard,
        text="Refresh",
        command=lambda:
        refresh_requests(tree)
    ).pack(pady=5)

    tk.Button(
        dashboard,
        text="Logout",
        bg="red",
        fg="black",
        command=dashboard.destroy
    ).pack(pady=10)


# ================= MAIN WINDOW =================

root = tk.Tk()
root.title("User Management System")
root.geometry("400x350")
root.config(bg="#dfe6e9")

tk.Label(
    root,
    text="Home Page",
    font=("Arial", 22, "bold"),
    bg="#dfe6e9"
).pack(pady=20)

tk.Label(
    root,
    text="Username",
    bg="#dfe6e9"
).pack()

username_entry = tk.Entry(root, width=30)
username_entry.pack(pady=5)

tk.Label(
    root,
    text="Password",
    bg="#dfe6e9"
).pack()

password_entry = tk.Entry(
    root,
    show="*",
    width=30
)
password_entry.pack(pady=5)

tk.Button(
    root,
    text="Login",
    width=20,
    bg="blue",
    fg="black",
    command=login
).pack(pady=10)

tk.Button(
    root,
    text="Sign Up",
    width=20,
    bg="green",
    fg="black",
    command=open_signup
).pack()

root.bind("<Return>", lambda event: login())

root.mainloop()