"""
Library Management System
A simple console-based application for managing library books and student records.
"""

import mysql.connector
from datetime import datetime, timedelta
from config import DB_CONFIG


def get_connection():
    """Create and return a database connection."""
    return mysql.connector.connect(**DB_CONFIG)


# ==================== STUDENT FUNCTIONS ====================

def add_student():
    """Add a new student to the database."""
    print("\n--- Add New Student ---")
    name = input("Enter student name: ")
    email = input("Enter email: ")
    phone = input("Enter phone: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, email, phone))
    conn.commit()
    
    print(f"✓ Student '{name}' added successfully!")
    cursor.close()
    conn.close()


def view_students():
    """Display all students."""
    print("\n--- All Students ---")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    
    if students:
        print(f"{'ID':<5} {'Name':<20} {'Email':<25} {'Phone':<15}")
        print("-" * 65)
        for s in students:
            print(f"{s[0]:<5} {s[1]:<20} {s[2]:<25} {s[3]:<15}")
    else:
        print("No students found.")
    
    cursor.close()
    conn.close()


def delete_student():
    """Delete a student by ID."""
    view_students()
    student_id = input("\nEnter student ID to delete: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print("✓ Student deleted successfully!")
    else:
        print("✗ Student not found.")
    
    cursor.close()
    conn.close()


# ==================== BOOK FUNCTIONS ====================

def add_book():
    """Add a new book to the database."""
    print("\n--- Add New Book ---")
    title = input("Enter book title: ")
    author = input("Enter author: ")
    isbn = input("Enter ISBN: ")
    quantity = input("Enter quantity: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "INSERT INTO books (title, author, isbn, quantity, available) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (title, author, isbn, quantity, quantity))
    conn.commit()
    
    print(f"✓ Book '{title}' added successfully!")
    cursor.close()
    conn.close()


def view_books():
    """Display all books."""
    print("\n--- All Books ---")
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    if books:
        print(f"{'ID':<5} {'Title':<25} {'Author':<20} {'ISBN':<18} {'Qty':<5} {'Avail':<5}")
        print("-" * 80)
        for b in books:
            print(f"{b[0]:<5} {b[1]:<25} {b[2]:<20} {b[3]:<18} {b[4]:<5} {b[5]:<5}")
    else:
        print("No books found.")
    
    cursor.close()
    conn.close()


def delete_book():
    """Delete a book by ID."""
    view_books()
    book_id = input("\nEnter book ID to delete: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM books WHERE book_id = %s", (book_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        print("✓ Book deleted successfully!")
    else:
        print("✗ Book not found.")
    
    cursor.close()
    conn.close()


# ==================== ISSUE/RETURN FUNCTIONS ====================

def issue_book():
    """Issue a book to a student."""
    print("\n--- Issue Book ---")
    view_books()
    book_id = input("\nEnter book ID to issue: ")
    
    view_students()
    student_id = input("\nEnter student ID: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if book is available
    cursor.execute("SELECT available, title FROM books WHERE book_id = %s", (book_id,))
    result = cursor.fetchone()
    
    if not result:
        print("✗ Book not found.")
        cursor.close()
        conn.close()
        return
    
    if result[0] <= 0:
        print("✗ Book is not available.")
        cursor.close()
        conn.close()
        return
    
    # Issue the book
    issue_date = datetime.now().date()
    return_date = issue_date + timedelta(days=14)  # 2 weeks loan period
    
    query = "INSERT INTO book_issues (book_id, student_id, issue_date, return_date, status) VALUES (%s, %s, %s, %s, 'issued')"
    cursor.execute(query, (book_id, student_id, issue_date, return_date))
    
    # Update available count
    cursor.execute("UPDATE books SET available = available - 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    
    print(f"✓ Book '{result[1]}' issued successfully!")
    print(f"  Return by: {return_date}")
    
    cursor.close()
    conn.close()


def return_book():
    """Return an issued book."""
    print("\n--- Return Book ---")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Show issued books
    query = """
        SELECT bi.issue_id, b.title, s.name, bi.issue_date, bi.return_date 
        FROM book_issues bi
        JOIN books b ON bi.book_id = b.book_id
        JOIN students s ON bi.student_id = s.student_id
        WHERE bi.status = 'issued'
    """
    cursor.execute(query)
    issues = cursor.fetchall()
    
    if not issues:
        print("No books currently issued.")
        cursor.close()
        conn.close()
        return
    
    print(f"{'Issue ID':<10} {'Book':<25} {'Student':<20} {'Issue Date':<12} {'Due Date':<12}")
    print("-" * 80)
    for i in issues:
        print(f"{i[0]:<10} {i[1]:<25} {i[2]:<20} {str(i[3]):<12} {str(i[4]):<12}")
    
    issue_id = input("\nEnter Issue ID to return: ")
    
    # Get book_id for the issue
    cursor.execute("SELECT book_id FROM book_issues WHERE issue_id = %s AND status = 'issued'", (issue_id,))
    result = cursor.fetchone()
    
    if not result:
        print("✗ Issue record not found or already returned.")
        cursor.close()
        conn.close()
        return
    
    book_id = result[0]
    
    # Update issue status
    cursor.execute("UPDATE book_issues SET status = 'returned' WHERE issue_id = %s", (issue_id,))
    
    # Update available count
    cursor.execute("UPDATE books SET available = available + 1 WHERE book_id = %s", (book_id,))
    conn.commit()
    
    print("✓ Book returned successfully!")
    
    cursor.close()
    conn.close()


def view_issued_books():
    """View all currently issued books."""
    print("\n--- Currently Issued Books ---")
    
    conn = get_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT bi.issue_id, b.title, s.name, bi.issue_date, bi.return_date 
        FROM book_issues bi
        JOIN books b ON bi.book_id = b.book_id
        JOIN students s ON bi.student_id = s.student_id
        WHERE bi.status = 'issued'
    """
    cursor.execute(query)
    issues = cursor.fetchall()
    
    if issues:
        print(f"{'Issue ID':<10} {'Book':<25} {'Student':<20} {'Issue Date':<12} {'Due Date':<12}")
        print("-" * 80)
        for i in issues:
            print(f"{i[0]:<10} {i[1]:<25} {i[2]:<20} {str(i[3]):<12} {str(i[4]):<12}")
    else:
        print("No books currently issued.")
    
    cursor.close()
    conn.close()


# ==================== MAIN MENU ====================

def main_menu():
    """Display main menu and handle user input."""
    while True:
        print("\n" + "=" * 40)
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1. Add Student")
        print("2. View Students")
        print("3. Delete Student")
        print("4. Add Book")
        print("5. View Books")
        print("6. Delete Book")
        print("7. Issue Book")
        print("8. Return Book")
        print("9. View Issued Books")
        print("0. Exit")
        print("=" * 40)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            delete_student()
        elif choice == '4':
            add_book()
        elif choice == '5':
            view_books()
        elif choice == '6':
            delete_book()
        elif choice == '7':
            issue_book()
        elif choice == '8':
            return_book()
        elif choice == '9':
            view_issued_books()
        elif choice == '0':
            print("Thank you for using Library Management System!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    print("Starting Library Management System...")
    main_menu()
