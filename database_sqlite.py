"""
Database module with SQLite for local testing
Handles all database interactions for student records
"""

import sqlite3
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    """Database handler for SQLite operations (local testing)"""
    
    def __init__(self, host=None, user=None, password=None, database='ryde_university.db'):
        """Initialize database connection parameters"""
        # For SQLite, we only need the database filename
        self.database = database
        self.connection = None
    
    def get_connection(self):
        """Get database connection (create if doesn't exist)"""
        try:
            if self.connection is None:
                self.connection = sqlite3.connect(self.database, check_same_thread=False)
                self.connection.row_factory = sqlite3.Row
                logger.info("Database connection established")
            return self.connection
        except Exception as e:
            logger.error(f"Error connecting to SQLite: {e}")
            raise
    
    def close_connection(self):
        """Close database connection"""
        if self.connection:
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
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                city TEXT NOT NULL,
                state TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
            
            cursor.execute(create_table_query)
            
            # Create indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_name ON students(name);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON students(email);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_city ON students(city);")
            
            connection.commit()
            logger.info("Database schema initialized successfully")
            
            # Insert sample data if table is empty
            cursor.execute("SELECT COUNT(*) FROM students")
            count = cursor.fetchone()[0]
            
            if count == 0:
                logger.info("Inserting sample student data")
                sample_data = [
                    ('John Doe', 'Example Address', 'Example City', 'example State', 'example@example.com', '9009009009'),
                    ('Jane Smith', '123 Main Street', 'Sydney', 'NSW', 'jane.smith@example.com', '0412345678'),
                    ('Mike Johnson', '456 Park Avenue', 'Melbourne', 'VIC', 'mike.johnson@example.com', '0423456789'),
                    ('Sarah Williams', '789 Beach Road', 'Brisbane', 'QLD', 'sarah.williams@example.com', '0434567890'),
                    ('David Brown', '321 Mountain View', 'Perth', 'WA', 'david.brown@example.com', '0445678901'),
                    ('Emily Davis', '654 Lake Drive', 'Adelaide', 'SA', 'emily.davis@example.com', '0456789012'),
                    ('James Wilson', '987 Forest Lane', 'Hobart', 'TAS', 'james.wilson@example.com', '0467890123'),
                    ('Olivia Taylor', '147 River Road', 'Canberra', 'ACT', 'olivia.taylor@example.com', '0478901234'),
                    ('William Anderson', '258 Hill Street', 'Darwin', 'NT', 'william.anderson@example.com', '0489012345'),
                    ('Sophia Martinez', '369 Valley Court', 'Gold Coast', 'QLD', 'sophia.martinez@example.com', '0490123456')
                ]
                
                cursor.executemany("""
                    INSERT INTO students (name, address, city, state, email, phone)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, sample_data)
                
                connection.commit()
                logger.info("Sample data inserted successfully")
            
            cursor.close()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def get_all_students(self):
        """Retrieve all students from database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            ORDER BY name ASC
            """
            
            cursor.execute(query)
            rows = cursor.fetchall()
            
            # Convert Row objects to dictionaries
            students = [dict(row) for row in rows]
            cursor.close()
            
            logger.info(f"Retrieved {len(students)} students")
            return students
        except Exception as e:
            logger.error(f"Error retrieving students: {e}")
            raise
    
    def get_student_by_id(self, student_id):
        """Retrieve a specific student by ID"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            WHERE id = ?
            """
            
            cursor.execute(query, (student_id,))
            row = cursor.fetchone()
            
            student = dict(row) if row else None
            cursor.close()
            
            return student
        except Exception as e:
            logger.error(f"Error retrieving student {student_id}: {e}")
            raise
    
    def add_student(self, name, address, city, state, email, phone):
        """Add a new student to the database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            INSERT INTO students (name, address, city, state, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            
            cursor.execute(query, (name, address, city, state, email, phone))
            connection.commit()
            
            student_id = cursor.lastrowid
            cursor.close()
            
            logger.info(f"Student added successfully with ID: {student_id}")
            return student_id
        except Exception as e:
            logger.error(f"Error adding student: {e}")
            raise
    
    def update_student(self, student_id, name, address, city, state, email, phone):
        """Update an existing student record"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            UPDATE students 
            SET name = ?, address = ?, city = ?, state = ?, 
                email = ?, phone = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """
            
            cursor.execute(query, (name, address, city, state, email, phone, student_id))
            connection.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                logger.info(f"Student {student_id} updated successfully")
                return True
            else:
                logger.warning(f"Student {student_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error updating student {student_id}: {e}")
            raise
    
    def delete_student(self, student_id):
        """Delete a student from the database"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = "DELETE FROM students WHERE id = ?"
            cursor.execute(query, (student_id,))
            connection.commit()
            
            rows_affected = cursor.rowcount
            cursor.close()
            
            if rows_affected > 0:
                logger.info(f"Student {student_id} deleted successfully")
                return True
            else:
                logger.warning(f"Student {student_id} not found")
                return False
        except Exception as e:
            logger.error(f"Error deleting student {student_id}: {e}")
            raise
    
    def search_students(self, search_term):
        """Search students by name, email, or city"""
        try:
            connection = self.get_connection()
            cursor = connection.cursor()
            
            query = """
            SELECT id, name, address, city, state, email, phone, 
                   created_at, updated_at 
            FROM students 
            WHERE name LIKE ? OR email LIKE ? OR city LIKE ?
            ORDER BY name ASC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern, search_pattern))
            rows = cursor.fetchall()
            
            students = [dict(row) for row in rows]
            cursor.close()
            
            logger.info(f"Search returned {len(students)} results")
            return students
        except Exception as e:
            logger.error(f"Error searching students: {e}")
            raise
