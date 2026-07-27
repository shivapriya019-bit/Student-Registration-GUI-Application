import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from openpyxl import Workbook
from datetime import date

# ================= DATABASE =================
conn = sqlite3.connect("students.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    mobile TEXT,
    gender TEXT,
    course TEXT,
    reg_date TEXT
)
""")
conn.commit()

# ================= MAIN APPLICATION =================
def main_app():
    root = tk.Tk()
    root.title("Vagdevi Technologies - Student Registration")
    root.geometry("500x580")
    root.config(bg="#f2f6ff")

    # Variables
    name = tk.StringVar()
    email = tk.StringVar()
    mobile = tk.StringVar()
    gender = tk.StringVar()
    course = tk.StringVar(value="Select Course")

    # ---------- FUNCTIONS ----------
    def clear_fields():
        name.set("")
        email.set("")
        mobile.set("")
        gender.set("")
        course.set("Select Course")

    def submit():
        if not all([name.get(), email.get(), mobile.get(), gender.get()]) or course.get() == "Select Course":
            messagebox.showerror("Error", "All fields are required")
            return

        if not mobile.get().isdigit() or len(mobile.get()) != 10:
            messagebox.showerror("Error", "Mobile number must be 10 digits")
            return

        cur.execute("""
            INSERT INTO students (name,email,mobile,gender,course,reg_date)
            VALUES (?,?,?,?,?,?)
        """, (
            name.get(), email.get(), mobile.get(),
            gender.get(), course.get(), str(date.today())
        ))
        conn.commit()
        messagebox.showinfo("Success", "Student Registered Successfully")
        #clear_fields()

    def view_students():
        win = tk.Toplevel(root)
        win.title("Student Records")
        win.geometry("1000x520")

        # Treeview Style
        style = ttk.Style()
        style.configure("Treeview.Heading",
                        background="yellow",
                        foreground="red",
                        font=("Arial", 10, "bold"))

        tree = ttk.Treeview(
            win,
            columns=("ID","Name","Email","Mobile","Gender","Course","Date"),
            show="headings"
        )
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center", width=130)

        def load_data(query="SELECT * FROM students", params=()):
            tree.delete(*tree.get_children())
            cur.execute(query, params)
            for row in cur.fetchall():
                tree.insert("", "end", values=row)

        load_data()

        # ---------- SEARCH ----------
        search_var = tk.StringVar()
        search_frame = tk.Frame(win)
        search_frame.pack(pady=5)

        tk.Entry(search_frame, textvariable=search_var, width=30).grid(row=0, column=0, padx=5)

        def search():
            load_data(
                "SELECT * FROM students WHERE name LIKE ? OR mobile LIKE ?",
                (f"%{search_var.get()}%", f"%{search_var.get()}%")
            )

        ttk.Button(search_frame, text="Search", command=search).grid(row=0, column=1)

        # ---------- FILTERS ----------
        filter_frame = tk.Frame(win)
        filter_frame.pack(pady=5)

        f_date = tk.StringVar()
        f_course = tk.StringVar(value="All")

        ttk.Label(filter_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        ttk.Entry(filter_frame, textvariable=f_date).grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Course:").grid(row=0, column=2)
        ttk.Combobox(
            filter_frame,
            textvariable=f_course,
            values=["All","Python","Java","Data Science","Web Development","AI & ML"],
            width=18
        ).grid(row=0, column=3, padx=5)

        # ---------- EXPORT ----------
        def export_excel():
            wb = Workbook()
            ws = wb.active
            ws.title = "Students"
            ws.append(["ID","Name","Email","Mobile","Gender","Course","Date"])

            query = "SELECT * FROM students WHERE 1=1"
            params = []
            filename_parts = ["students"]

            if f_course.get() != "All":
                query += " AND course=?"
                params.append(f_course.get())
                filename_parts.append(f_course.get().replace(" ", "_"))

            if f_date.get():
                query += " AND reg_date=?"
                params.append(f_date.get())
                filename_parts.append(f_date.get())

            cur.execute(query, params)
            rows = cur.fetchall()

            if not rows:
                messagebox.showwarning("No Data", "No records found")
                return

            for r in rows:
                ws.append(r)

            filename = "_".join(filename_parts) + ".xlsx"
            wb.save(filename)
            messagebox.showinfo("Exported", f"Excel file created:\n{filename}")

        ttk.Button(win, text="Export to Excel", command=export_excel).pack(pady=5)

        tk.Label(
            win,
            text="Developed by @VCS IT Solutions Pvt Ltd",
            fg="gray"
        ).pack(side="bottom", pady=5)

    # ---------- UI ----------
    tk.Label(
        root, text="Vagdevi Technologies",
        font=("Arial", 18, "bold"),
        fg="#2c3e50", bg="#f2f6ff"
    ).pack(pady=5)

    frame = tk.Frame(root, bg="white", bd=2, relief="groove")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    def field(label, var):
        tk.Label(frame, text=label, fg="#2980b9", bg="white").pack(anchor="w", padx=10)
        tk.Entry(frame, textvariable=var).pack(fill="x", padx=10, pady=3)

    field("Name", name)
    field("Email", email)
    field("Mobile Number", mobile)

    tk.Label(frame, text="Gender", fg="#2980b9", bg="white").pack(anchor="w", padx=10)
    g = tk.Frame(frame, bg="white")
    g.pack(anchor="w", padx=10)
    for opt in ["Male", "Female", "Others"]:
        tk.Radiobutton(g, text=opt, variable=gender, value=opt, bg="white").pack(side="left", padx=10)

    tk.Label(frame, text="Course", fg="#2980b9", bg="white").pack(anchor="w", padx=10)
    tk.OptionMenu(
        frame, course,
        "Python","Java","Data Science","Web Development","AI & ML"
    ).pack(fill="x", padx=10)

    btn = tk.Frame(root, bg="#f2f6ff")
    btn.pack(pady=10)

    tk.Button(btn, text="Submit", bg="#27ae60", fg="white",
              width=12, command=submit).grid(row=0, column=0, padx=5)
    tk.Button(btn, text="Clear", bg="#f1c40f",
              width=12, command=clear_fields).grid(row=0, column=1, padx=5)
    tk.Button(btn, text="View Records", bg="#3498db", fg="white",
              width=12, command=view_students).grid(row=1, column=0, pady=5)
    tk.Button(btn, text="Logout", bg="#e74c3c", fg="white",
              width=12, command=root.destroy).grid(row=1, column=1, pady=5)

    tk.Label(
        root,
        text="Developed by @VCS IT Solutions Pvt Ltd",
        fg="gray", bg="#f2f6ff"
    ).pack(side="bottom", pady=5)

    root.mainloop()

# ================= LOGIN WINDOW =================
login_win = tk.Tk()
login_win.title("Login - Vagdevi Technologies")
login_win.geometry("350x260")

user = tk.StringVar()
pwd = tk.StringVar()

def login():
    if user.get() == "admin" and pwd.get() == "admin123":
        login_win.destroy()
        main_app()
    else:
        messagebox.showerror("Login Failed", "Invalid Credentials")

tk.Label(login_win, text="Vagdevi Technologies",
         font=("Arial", 16, "bold"), fg="#2c3e50").pack(pady=10)

tk.Label(login_win, text="Username", fg="blue").pack()
tk.Entry(login_win, textvariable=user).pack()

tk.Label(login_win, text="Password", fg="blue").pack()
tk.Entry(login_win, textvariable=pwd, show="*").pack()

tk.Button(login_win, text="Login", bg="#4CAF50",
          fg="white", width=15, command=login).pack(pady=15)

tk.Label(
    login_win,
    text="Developed by @VCS IT Solutions Pvt Ltd",
    fg="gray"
).pack(side="bottom", pady=5)

login_win.mainloop()
