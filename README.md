# Student Registration System (Tkinter + SQLite)

A desktop application built with Python's Tkinter for registering students and managing their records. Data is stored in a local SQLite database, and records can be exported to Excel, filtered by course and date.

## Features

- Admin login screen
- Student registration form: name, email, mobile number, gender, course
- Registration date captured automatically
- Input validation: all fields required, mobile number must be exactly 10 digits
- Records window with a table view (Treeview)
- Search by name or mobile number
- Course and date filters
- Excel export (OpenPyXL) filtered by course and date, with dynamic file names, for example `students_Python_2026-11-17.xlsx`
- SQLite storage using parameterized queries to prevent SQL injection

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3 | Core language |
| Tkinter | Graphical user interface |
| SQLite (sqlite3) | Database storage |
| OpenPyXL | Excel report generation |

## Project Structure

```
student-Registration-GUI-Application/
├── student_.py      # Main application (login, registration, records, export)
├── students.db      # SQLite database (created automatically on first run)
└── README.md
```

## Installation and Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/shivapriya019-bit/student-Registration-GUI-Application.git
   cd student-Registration-GUI-Application
   ```

2. Install the required library (Tkinter and sqlite3 come with Python):

   ```bash
   pip install openpyxl
   ```

3. Run the application:

   ```bash
   python student_.py
   ```

4. Log in with the default admin credentials:

   - Username: `admin`
   - Password: `admin123`

## How to Use

1. **Register a student:** fill in the form and click **Submit**.
2. **View records:** click **View Records** to open the records window.
3. **Search:** type a name or mobile number and click **Search**.
4. **Export to Excel:** choose a course and/or enter a date (YYYY-MM-DD), then click **Export to Excel**. The file is saved in the project folder.

## Database Schema

Table: `students`

| Column | Type | Description |
|---|---|---|
| id | INTEGER | Primary key, auto-increment |
| name | TEXT | Student name |
| email | TEXT | Email address |
| mobile | TEXT | 10-digit mobile number |
| gender | TEXT | Male / Female / Others |
| course | TEXT | Selected course |
| reg_date | TEXT | Registration date (YYYY-MM-DD) |

## Known Limitations

- The login uses fixed credentials in the code. It is meant for demonstration, not production.
- The course and date filters apply to the Excel export, not to the table on screen.
- Update and delete operations are not implemented yet.

## Future Improvements

- Edit and delete student records
- Users table with hashed passwords
- Email format validation and duplicate checks
- Filters that update the on-screen table
- PDF reports
- Package the app as a `.exe` file

## Author

**Shivapriya**
GitHub: [shivapriya019-bit](https://github.com/shivapriya019-bit)
LinkedIn: [shivapriya05](https://linkedin.com/in/shivapriya05)
# Student-Registration-GUI-Application
