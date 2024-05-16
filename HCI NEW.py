import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def center_window(window, width, height):
    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate x and y coordinates to center the window
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    # Set the window geometry
    window.geometry('%dx%d+%d+%d' % (width, height, x, y))

def create_database():
    # Connect to the SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('driving_school.db')
    c = conn.cursor()

    # Create tables for students, instructors, and courses if they don't exist
    c.execute('''CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    age INTEGER,
                    mobile_number TEXT,
                    address TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS instructors (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    specialization TEXT
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY,
                    course TEXT,
                    price INTEGER
                )''')

    # Commit changes and close the connection
    conn.commit()
    conn.close()

def open_manage_students():
    def save_student():
        name = name_entry.get()
        age = age_entry.get()
        mobile_number = mobile_entry.get()
        address = address_entry.get()

        # Connect to the SQLite database
        conn = sqlite3.connect('driving_school.db')
        c = conn.cursor()

        # Insert student data into the database
        c.execute('''INSERT INTO students (name, age, mobile_number, address)
                    VALUES (?, ?, ?, ?)''', (name, age, mobile_number, address))

        # Commit changes
        conn.commit()

        # Get the ID of the last inserted row
        student_id = c.lastrowid

        # Close the connection
        conn.close()

        # Update the Treeview with the new student data
        students_tree.insert('', tk.END, values=(student_id, name, age, mobile_number, address))

        messagebox.showinfo("Success", "Student details saved successfully!")

    def delete_student():
        # Get the selected item from the Treeview
        selected_item = students_tree.selection()

        if selected_item:
            # Get the student ID from the selected item
            student_id = students_tree.item(selected_item)['values'][0]

            # Connect to the SQLite database
            conn = sqlite3.connect('driving_school.db')
            c = conn.cursor()

            # Delete the student from the database
            c.execute("DELETE FROM students WHERE id=?", (student_id,))

            # Commit changes
            conn.commit()

            # Close the connection
            conn.close()

            # Remove the selected item from the Treeview
            students_tree.delete(selected_item)

            messagebox.showinfo("Success", "Student details deleted successfully!")
        else:
            messagebox.showerror("Error", "Please select a student to delete!")

    manage_students_window = tk.Toplevel(root)
    manage_students_window.title("Manage Students")
    manage_students_window.configure(bg="light blue")
    center_window(manage_students_window, 800, 600)

    # Add manage students content
    tk.Label(manage_students_window, text="Manage Students", font=("Helvetica", 16), bg="light blue").pack(pady=10)

    # Entry fields
    tk.Label(manage_students_window, text="Name:", bg="light blue").pack()
    name_entry = tk.Entry(manage_students_window)
    name_entry.pack()

    tk.Label(manage_students_window, text="Age:", bg="light blue").pack()
    age_entry = tk.Entry(manage_students_window)
    age_entry.pack()

    tk.Label(manage_students_window, text="Mobile Number:", bg="light blue").pack()
    mobile_entry = tk.Entry(manage_students_window)
    mobile_entry.pack()

    tk.Label(manage_students_window, text="Address:", bg="light blue").pack()
    address_entry = tk.Entry(manage_students_window)
    address_entry.pack()

    # Save Button
    save_button = tk.Button(manage_students_window, text="Save", width=10, height=2, command=save_student)
    save_button.pack(pady=10)

    # Listbox to display students
    students_tree = ttk.Treeview(manage_students_window, columns=('ID', 'Name', 'Age', 'Mobile Number', 'Address'), show='headings')
    students_tree.heading('ID', text='ID')
    students_tree.heading('Name', text='Name')
    students_tree.heading('Age', text='Age')
    students_tree.heading('Mobile Number', text='Mobile Number')
    students_tree.heading('Address', text='Address')
    students_tree.pack(pady=10)

    # Delete Button
    delete_button = tk.Button(manage_students_window, text="Delete", width=10, height=2, command=delete_student)
    delete_button.pack(pady=10)

def open_manage_courses():
    manage_courses_window = tk.Toplevel(root)
    manage_courses_window.title("Manage Courses")
    manage_courses_window.configure(bg="light blue")
    center_window(manage_courses_window, 600, 500)

    # Add manage courses content
    tk.Label(manage_courses_window, text="Manage Courses", font=("Helvetica", 16), bg="light blue").pack(pady=10)

    # Create Treeview to display courses and prices
    courses_tree = ttk.Treeview(manage_courses_window, columns=('ID','Course', 'Price'), show='headings')
    courses_tree.heading('ID', text='ID')
    courses_tree.heading('Course', text='Course')
    courses_tree.heading('Price', text='Price')

    # Example course data (replace with data from the database)
    courses_data = [
        ('1', 'Introductory', '100'),
        ('2', 'Standard', '250'),
        ('3', 'Pass Plus', '500')
    ]

    # Insert courses and prices into the Treeview
    for course in courses_data:
        courses_tree.insert('', tk.END, values=course)

    courses_tree.pack(pady=10)

def open_manage_instructors():
    manage_instructors_window = tk.Toplevel(root)
    manage_instructors_window.title("Manage Instructors")
    manage_instructors_window.configure(bg="light blue")
    center_window(manage_instructors_window, 1000, 800)

    # Add manage instructors content
    tk.Label(manage_instructors_window, text="Manage Instructors", font=("Helvetica", 16), bg="light blue").pack(pady=10)

    # Create Treeview to display instructors
    instructors_tree = ttk.Treeview(manage_instructors_window, columns=('ID', 'Name', 'Email', 'Phone', 'Specialization'), show='headings')
    instructors_tree.heading('ID', text='ID')
    instructors_tree.heading('Name', text='Name')
    instructors_tree.heading('Email', text='Email')
    instructors_tree.heading('Phone', text='Phone')
    instructors_tree.heading('Specialization', text='Specialization')

    # Example instructor data (replace with data from the database)
    instructors_data = [
        ('1', 'John Doe', 'john@example.com', '1234567890', 'Beginner'),
        ('2', 'Jane Smith', 'jane@example.com', '9876543210', 'Advanced'),
        ('3', 'Alex Johnson', 'alex@example.com', '4561237890', 'Defensive Driving')
    ]

    # Insert instructor data into the Treeview
    for instructor in instructors_data:
        instructors_tree.insert('', tk.END, values=instructor)

    instructors_tree.pack(pady=10)

def dummy_function():
    messagebox.showinfo("Info", "This functionality is under development!")

# Main Welcome Screen
root = tk.Tk()
root.title("Welcome to Driving School")
root.geometry("600x400")
root.configure(bg="light yellow")

center_window(root,600, 400)

# Driving School Name
tk.Label(root, text="SASI Driving School", font=("Helvetica", 24), bg="light yellow").pack(pady=20)

# Admin Button
admin_button = tk.Button(root, text="Admin", font=("Helvetica", 18), width=10, height=2, command=lambda: admin_login(600, 400))
admin_button.pack(pady=40)

def admin_login(welcome_width, welcome_height):
    def validate_login():
        if username_entry.get() == "admin" and password_entry.get() == "password":
            login_window.destroy()
            open_admin_menu()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.configure(bg="light blue")  # Set background color
    center_window(login_window, welcome_width, welcome_height)

    # Username Label and Entry
    username_label = tk.Label(login_window, text="Username:", bg="light blue",font=("Helvetica", 14))
    username_label.place(relx=0.5, rely=0.32, anchor=tk.CENTER)
    username_entry = tk.Entry(login_window)
    username_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    # Password Label and Entry
    password_label = tk.Label(login_window, text="Password:", bg="light blue",font=("Helvetica", 14))
    password_label.place(relx=0.5, rely=0.52, anchor=tk.CENTER)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    # Login Button
    login_button = tk.Button(login_window, text="Login", width=10, height=2, command=validate_login)
    login_button.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    # Create the database when logging in
    create_database()

def open_admin_menu():
    # Destroy previous frame if exists
    if hasattr(root, "current_frame"):
        root.current_frame.destroy()

    # Create new window for Admin Menu
    admin_menu_window = tk.Toplevel(root)
    admin_menu_window.title("Admin Menu")
    admin_menu_window.configure(bg="light yellow")  # Set background color
    center_window(admin_menu_window, 400, 300)

    # Add admin menu content
    tk.Label(admin_menu_window, text="Admin Menu", font=("Helvetica", 16), bg="light yellow").grid(row=1, column=1,pady=5)
    # Draw a layout line
    ttk.Separator(admin_menu_window, orient="horizontal").grid(row=2, columnspan=3, sticky="ew", pady=10)
    tk.Button(admin_menu_window, text="Manage Students", width=20, height=2, command=open_manage_students).grid(row=2, column=2,pady=5)
    tk.Button(admin_menu_window, text="Manage Courses", width=20, height=2, command=open_manage_courses).grid(row=3, column=2,pady=5)
    tk.Button(admin_menu_window, text="Manage Instructors", width=20, height=2, command=open_manage_instructors).grid(row=4, column=2,pady=5)
    tk.Button(admin_menu_window, text="Logout", width=20, height=2, command=logout).grid(row=5, column=2,pady=5)

    # Set current frame
    root.current_frame = admin_menu_window

def logout():
    # Destroy the root window
    root.destroy()
    # Open the login window again

root.mainloop()
