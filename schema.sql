-- Ryde University Student Records Database Schema
-- MySQL 8.0

-- Create database
CREATE DATABASE IF NOT EXISTS ryde_university
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ryde_university;

-- Create students table
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
    INDEX idx_city (city),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert sample data
INSERT INTO students (name, address, city, state, email, phone) VALUES
('John Doe', 'Example Address', 'Example City', 'example State', 'example@example.com', '9009009009'),
('Jane Smith', '123 Main Street', 'Sydney', 'NSW', 'jane.smith@example.com', '0412345678'),
('Mike Johnson', '456 Park Avenue', 'Melbourne', 'VIC', 'mike.johnson@example.com', '0423456789'),
('Sarah Williams', '789 Beach Road', 'Brisbane', 'QLD', 'sarah.williams@example.com', '0434567890'),
('David Brown', '321 Mountain View', 'Perth', 'WA', 'david.brown@example.com', '0445678901'),
('Emily Davis', '654 Lake Drive', 'Adelaide', 'SA', 'emily.davis@example.com', '0456789012'),
('James Wilson', '987 Forest Lane', 'Hobart', 'TAS', 'james.wilson@example.com', '0467890123'),
('Olivia Taylor', '147 River Road', 'Canberra', 'ACT', 'olivia.taylor@example.com', '0478901234'),
('William Anderson', '258 Hill Street', 'Darwin', 'NT', 'william.anderson@example.com', '0489012345'),
('Sophia Martinez', '369 Valley Court', 'Gold Coast', 'QLD', 'sophia.martinez@example.com', '0490123456');

-- Create user for application (use strong password in production)
-- Run these commands as MySQL root user:
-- CREATE USER 'ryde_user'@'localhost' IDENTIFIED BY 'ryde_password';
-- GRANT ALL PRIVILEGES ON ryde_university.* TO 'ryde_user'@'localhost';
-- FLUSH PRIVILEGES;

-- For AWS RDS, use these commands:
-- CREATE USER 'ryde_user'@'%' IDENTIFIED BY 'strong_password_here';
-- GRANT ALL PRIVILEGES ON ryde_university.* TO 'ryde_user'@'%';
-- FLUSH PRIVILEGES;
