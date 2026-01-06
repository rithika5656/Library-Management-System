-- Library Management System Database Setup
-- Run this file in MySQL to create the database and tables

CREATE DATABASE IF NOT EXISTS library_db;
USE library_db;

-- Students table
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Books table
CREATE TABLE IF NOT EXISTS books (
    book_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100),
    isbn VARCHAR(20),
    quantity INT DEFAULT 1,
    available INT DEFAULT 1
);

-- Book Issues table
CREATE TABLE IF NOT EXISTS book_issues (
    issue_id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT,
    student_id INT,
    issue_date DATE,
    return_date DATE,
    status VARCHAR(20) DEFAULT 'issued',
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

-- Sample data
INSERT INTO students (name, email, phone) VALUES
('John Doe', 'john@email.com', '1234567890'),
('Jane Smith', 'jane@email.com', '0987654321'),
('Bob Wilson', 'bob@email.com', '5555555555');

INSERT INTO books (title, author, isbn, quantity, available) VALUES
('Python Programming', 'John Smith', '978-0-13-110362-7', 5, 5),
('Data Structures', 'Jane Doe', '978-0-201-63361-0', 3, 3),
('Database Systems', 'Bob Author', '978-0-07-120457-8', 4, 4),
('Web Development', 'Alice Writer', '978-0-596-51774-8', 2, 2);
