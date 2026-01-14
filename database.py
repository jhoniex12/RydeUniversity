"""
Database module for MySQL operations
Handles all database interactions for student records
"""

import mysql.connector
from mysql.connector import Error
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Database handler for MySQL operations"""
    
    def __init__(self, host, user, password, database):
        """Initialize database connection parameters"""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
    
    def get_connection(self):
        """Get database connection (create if doesn't exist)"""
        try:
            if self.connection is None or not self.connection.is_connected():
                self.connection = mysql.connector.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    autocommit=True
                )
                logger.info("Database connection established")
            return self.connection
        except Error as e:
            logger.error(f"Error connecting to MySQL: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
    
    def init_database(self):
        """Initialize database schema"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            # Create students table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                address VARCHAR(255) NOT NULL,
                city VARCHAR(100) NOT NULL,
                state VARCHAR(100) NOT NULL,
                email VARCHAR(255) NOT NULL UNIQUE,
                phone VARCHAR(20) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_name (name),
                INDEX idx_email (email),
                INDEX idx_city (city)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            cursor.execute(create_table_query)
            logger.info("Database schema initialized successfully")
            
            # Insert sample data if table is empty
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("Inserting sample student data")
                sample_data = """
                INSERT INTO students (name, address, city, state, email, phone) VALUES
                ('John Doe', 'Example Address', 'Example City', 'example State', 'example@example.com', '9009009009'),
                ('Jane Smith', '123 Main Street', 'Sydney', 'NSW', 'jane.smith@example.com', '0412345678'),
                ('Mike Johnson', '456 Park Avenue', 'Melbourne', 'VIC', 'mike.johnson@example.com', '0423456789'),
                ('Sarah Williams', '789 Beach Road', 'Brisbane', 'QLD', 'sarah.williams@example.com', '0434567890'),
                ('David Brown', '321 Mountain View', 'Perth', 'WA', 'david.brown@example.com', '0445678901');
                """
                cursor.execute(sample_data)
                logger.info("Sample data inserted successfully")
            
            cursor.close()
        except Error as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_all_students(self):
        """Retrieve all students from database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            ORDER BY name ASC
            """
            
            cursor.execute(query)
            students = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Retrieved {len(students)} students")
            return students
        except Error as e:
            logger.error(f"Error retrieving students: {e}")
            raise
    
    def get_student_by_id(self, student_id):
        """Retrieve a specific student by ID"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            WHERE id = %s
            """
            
            cursor.execute(query, (student_id,))
            student = cursor.fetchone()
            cursor.close()
            
            return student
        except Error as e:
            logger.error(f"Error retrieving student {student_id}: {e}")
            raise
    
    def add_student(self, name, address, city, state, email, phone):
        """Add a new student to the database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO students (name, address, city, state, email, phone)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            values = (name, address, city, state, email, phone)
            cursor.execute(query, values)
            
            student_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"Student added successfully with ID: {student_id}")
            return student_id
        except Error as e:
            logger.error(f"Error adding student: {e}")
            raise
    
    def update_student(self, student_id, name, address, city, state, email, phone):
        """Update an existing student record"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            UPDATE students 
            SET name = %s, address = %s, city = %s, state = %s, 
                email = %s, phone = %s
            WHERE id = %s
            """
            
            values = (name, address, city, state, email, phone, student_id)
            cursor.execute(query, values)
            
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                logger.info(f"Student {student_id} updated successfully")
                return True
            else:
                logger.warning(f"Student {student_id} not found")
                return False
        except Error as e:
            logger.error(f"Error updating student {student_id}: {e}")
            raise
    
    def delete_student(self, student_id):
        """Delete a student from the database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM students WHERE id = %s"
            cursor.execute(query, (student_id,))
            
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                logger.info(f"Student {student_id} deleted successfully")
                return True
            else:
                logger.warning(f"Student {student_id} not found")
                return False
        except Error as e:
            logger.error(f"Error deleting student {student_id}: {e}")
            raise
    
    def search_students(self, search_term):
        """Search students by name, email, or city"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            WHERE name LIKE %s OR email LIKE %s OR city LIKE %s
            ORDER BY name ASC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            students = cursor.fetchall()
            cursor.close()
            
            logger.info(f"Search returned {len(students)} results")
            return students
        except Error as e:
            logger.error(f"Error searching students: {e}")
            raise
