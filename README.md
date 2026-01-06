# Library Management System

A simple console-based Library Management System built with Python and MySQL.

## Features

- **Student Management**: Add, view, and delete student records
- **Book Management**: Add, view, and delete books
- **Book Issue/Return**: Issue books to students and process returns
- **Track Issued Books**: View all currently issued books

## Prerequisites

- Python 3.x
- MySQL Server
- mysql-connector-python

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/rithika5656/Library-Management-System.git
   cd Library-Management-System
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup MySQL Database**
   - Start MySQL server
   - Run the SQL script to create database and tables:
   ```bash
   mysql -u root -p < database.sql
   ```

4. **Configure Database Connection**
   - Open `config.py`
   - Update the `password` field with your MySQL password

## Usage

Run the application:
```bash
python library.py
```

## Menu Options

1. Add Student
2. View Students
3. Delete Student
4. Add Book
5. View Books
6. Delete Book
7. Issue Book
8. Return Book
9. View Issued Books
0. Exit

## Database Schema

- **students**: student_id, name, email, phone, created_at
- **books**: book_id, title, author, isbn, quantity, available
- **book_issues**: issue_id, book_id, student_id, issue_date, return_date, status

## License

MIT License
