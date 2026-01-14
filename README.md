<<<<<<< HEAD

# Ryde University Student Records Web Application

A scalable, high-performance web application for managing student admission records, designed to run on AWS infrastructure with MySQL 8.0 database.

## Features

- ✅ **View** all student records with pagination support
- ✅ **Add** new student applications
- ✅ **Update** existing student records
- ✅ **Delete** student records
- ✅ **Search** students by name, email, or city
- ✅ **RESTful API** for all operations
- ✅ **Health check** endpoint for load balancer monitoring
- ✅ **MySQL 8.0** database with optimized indexes
- ✅ **Responsive design** for mobile and desktop

## Technology Stack

- **Backend:** Python 3.9+ with Flask
- **Database:** MySQL 8.0 (Amazon RDS Multi-AZ)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Server:** Gunicorn (production)
- **Cloud:** AWS (EC2, RDS, ALB, Auto Scaling)

## Architecture Alignment

This application is designed to run in the AWS architecture specified in `AWS_Architecture_Design_Solution.md`:

- **Compute:** Runs on EC2 instances (t3.medium) behind Application Load Balancer
- **Database:** Connects to RDS MySQL 8.0 Multi-AZ deployment in private subnets
- **Security:** Uses AWS Secrets Manager for database credentials (in production)
- **Monitoring:** Health check endpoint (`/health`) for ALB target health checks
- **Scalability:** Stateless design enables horizontal scaling with Auto Scaling Group

## Prerequisites

### For Local Development:

- Python 3.9 or higher
- MySQL 8.0
- pip (Python package manager)

### For AWS Production Deployment:

- AWS Account with appropriate permissions
- RDS MySQL 8.0 instance (Multi-AZ)
- EC2 instances with Python 3.9+
- Application Load Balancer
- AWS Secrets Manager (for credentials)

## Installation

### 1. Clone or Download the Application

```bash
cd ryde-university-app
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

**Option A: Local MySQL**

```bash
# Connect to MySQL as root
mysql -u root -p

# Run the schema script
mysql -u root -p < schema.sql

# Or copy and paste commands from schema.sql
```

**Option B: AWS RDS MySQL**

```bash
# Connect to RDS instance
mysql -h your-rds-endpoint.ap-southeast-2.rds.amazonaws.com -u admin -p

# Run schema commands from schema.sql
```

### 5. Configure Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```env
# For local development
DB_HOST=localhost
DB_USER=ryde_user
DB_PASSWORD=ryde_password
DB_NAME=ryde_university

# For AWS RDS
DB_HOST=ryde-db.xxxxxxxxxxxx.ap-southeast-2.rds.amazonaws.com
DB_USER=ryde_admin
DB_PASSWORD=your-rds-password
DB_NAME=ryde_university
```

### 6. Run the Application

**Development Mode:**

```bash
python app.py
```

**Production Mode (with Gunicorn):**

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

The application will be available at: http://localhost:5000

## API Endpoints

### REST API

| Method | Endpoint             | Description          |
| ------ | -------------------- | -------------------- |
| GET    | `/api/students`      | Get all students     |
| GET    | `/api/students/<id>` | Get student by ID    |
| POST   | `/api/students`      | Add new student      |
| PUT    | `/api/students/<id>` | Update student       |
| DELETE | `/api/students/<id>` | Delete student       |
| GET    | `/health`            | Health check for ALB |

### Web Pages

| Route       | Description                    |
| ----------- | ------------------------------ |
| `/`         | Home page with student list    |
| `/students` | Students list page with search |

### API Examples

**Add Student:**

```bash
curl -X POST http://localhost:5000/api/students \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "address": "123 Main St",
    "city": "Sydney",
    "state": "NSW",
    "email": "john@example.com",
    "phone": "0412345678"
  }'
```

**Update Student:**

```bash
curl -X PUT http://localhost:5000/api/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Updated",
    "address": "456 New St",
    "city": "Melbourne",
    "state": "VIC",
    "email": "john.updated@example.com",
    "phone": "0423456789"
  }'
```

**Delete Student:**

```bash
curl -X DELETE http://localhost:5000/api/students/1
```

**Health Check:**

```bash
curl http://localhost:5000/health
```

## Database Schema

```sql
CREATE TABLE students (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

## AWS Deployment Guide

### 1. Prepare EC2 Instance

```bash
# Update system
sudo yum update -y

# Install Python 3.9
sudo yum install python3.9 -y

# Install MySQL client
sudo yum install mysql -y

# Install git
sudo yum install git -y
```

### 2. Deploy Application

```bash
# Clone application
git clone <repository-url>
cd ryde-university-app

# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure for RDS

Set environment variables or use AWS Secrets Manager:

```bash
export DB_HOST=ryde-db.xxxxxxxxxxxx.ap-southeast-2.rds.amazonaws.com
export DB_USER=ryde_admin
export DB_PASSWORD=$(aws secretsmanager get-secret-value --secret-id ryde-db-password --query SecretString --output text)
export DB_NAME=ryde_university
```

### 4. Run with Systemd (Production)

Create `/etc/systemd/system/ryde-app.service`:

```ini
[Unit]
Description=Ryde University Student Records Application
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/ryde-university-app
Environment="PATH=/home/ec2-user/ryde-university-app/venv/bin"
EnvironmentFile=/home/ec2-user/ryde-university-app/.env
ExecStart=/home/ec2-user/ryde-university-app/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable ryde-app
sudo systemctl start ryde-app
sudo systemctl status ryde-app
```

### 5. Configure ALB Health Checks

- **Health Check Path:** `/health`
- **Interval:** 30 seconds
- **Timeout:** 5 seconds
- **Healthy Threshold:** 2
- **Unhealthy Threshold:** 3

## Performance Optimization

### Database Optimization

1. **Indexes:** Already configured on `name`, `email`, and `city` columns
2. **Connection Pooling:** Implemented via mysql-connector-python
3. **Query Optimization:** Uses prepared statements to prevent SQL injection

### Application Optimization

1. **Stateless Design:** No server-side sessions, enables horizontal scaling
2. **Connection Reuse:** Database connections reused across requests
3. **Error Handling:** Graceful error handling with proper logging

### AWS-Specific Optimizations

1. **Auto Scaling:** Application designed for horizontal scaling
2. **Load Balancing:** Health checks ensure traffic only to healthy instances
3. **Database:** RDS Multi-AZ for automatic failover
4. **Caching:** Can add ElastiCache (Redis) for session/query caching

## Security Features

### Implemented

- ✅ SQL injection prevention (prepared statements)
- ✅ Input validation on all forms
- ✅ Unique email constraint
- ✅ Connection encryption (SSL/TLS) to RDS
- ✅ Environment-based configuration
- ✅ No hardcoded credentials

### Production Recommendations

- 🔒 Use AWS Secrets Manager for database credentials
- 🔒 Enable SSL/TLS for MySQL connections
- 🔒 Implement rate limiting
- 🔒 Add CSRF protection
- 🔒 Enable Content Security Policy (CSP)
- 🔒 Use HTTPS (handled by ALB)
- 🔒 Implement authentication and authorization

## Monitoring

### Application Metrics

- Request count and latency (via Flask)
- Database query performance
- Error rates

### AWS CloudWatch Integration

Monitor these metrics:

- EC2 CPU utilization
- Database connections
- Request count (from ALB)
- Target health status

### Logging

Application logs to stdout (captured by CloudWatch Logs):

- Database connection events
- CRUD operations
- Errors and exceptions

## Troubleshooting

### Database Connection Issues

```bash
# Test MySQL connection
mysql -h DB_HOST -u DB_USER -p

# Check if RDS security group allows EC2 access
# Verify Security Group inbound rules allow port 3306 from EC2 security group
```

### Application Not Starting

```bash
# Check logs
sudo journalctl -u ryde-app -n 50

# Verify dependencies
pip list

# Test database connection
python -c "from database import Database; db = Database('host', 'user', 'pass', 'db'); print('Connected')"
```

### Health Check Failing

```bash
# Test health endpoint
curl http://localhost:5000/health

# Check database connectivity
mysql -h DB_HOST -u DB_USER -p -e "SELECT 1"
```

## Performance Testing

Test application performance:

```bash
# Install Apache Bench
sudo yum install httpd-tools -y

# Test with 100 concurrent requests
ab -n 1000 -c 100 http://localhost:5000/

# Test API endpoint
ab -n 1000 -c 100 -p student.json -T application/json http://localhost:5000/api/students
```

## License

Proprietary - Ryde University

## Support

For issues or questions, contact: IT Support <support@ryde.university.edu.au>

---

# **Note:** This application is designed to work with the AWS architecture described in `AWS_Architecture_Design_Solution.md`. Ensure all AWS resources (VPC, RDS, EC2, ALB) are properly configured before deployment.

# RydeUniversity

> > > > > > > 04f82911cd3e489d35f4b2e98a85678e8c30fe4f
