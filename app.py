"""
Ryde University Student Records Web Application
Flask-based web application for managing student records
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from database import Database
import os
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database connection
db = Database(
    host=app.config['DB_HOST'],
    user=app.config['DB_USER'],
    password=app.config['DB_PASSWORD'],
    database=app.config['DB_NAME']
)

@app.route('/')
def index():
    """Home page - Display all students"""
    try:
        students = db.get_all_students()
        return render_template('index.html', students=students)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/students')
def students_list():
    """Students list page - Display all students"""
    try:
        students = db.get_all_students()
        return render_template('students.html', students=students)
    except Exception as e:
        return render_template('error.html', error=str(e)), 500

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """API endpoint to get all students"""
    try:
        students = db.get_all_students()
        return jsonify({'success': True, 'data': students})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """API endpoint to get a specific student"""
    try:
        student = db.get_student_by_id(student_id)
        if student:
            return jsonify({'success': True, 'data': student})
        else:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students', methods=['POST'])
def api_add_student():
    """API endpoint to add a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'city', 'state', 'email', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        student_id = db.add_student(
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            email=data['email'],
            phone=data['phone']
        )
        
        return jsonify({'success': True, 'message': 'Student added successfully', 'id': student_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
def api_update_student(student_id):
    """API endpoint to update a student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'address', 'city', 'state', 'email', 'phone']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'success': False, 'error': f'Missing required field: {field}'}), 400
        
        success = db.update_student(
            student_id=student_id,
            name=data['name'],
            address=data['address'],
            city=data['city'],
            state=data['state'],
            email=data['email'],
            phone=data['phone']
        )
        
        if success:
            return jsonify({'success': True, 'message': 'Student updated successfully'})
        else:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def api_delete_student(student_id):
    """API endpoint to delete a student"""
    try:
        success = db.delete_student(student_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Student deleted successfully'})
        else:
            return jsonify({'success': False, 'error': 'Student not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint for load balancer"""
    try:
        # Test database connection
        db.get_connection().ping(reconnect=True)
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 503

@app.errorhandler(404)
def not_found(error):
    """404 error handler"""
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    return render_template('error.html', error='Internal server error'), 500

if __name__ == '__main__':
    # Initialize database tables
    db.init_database()
    
    # Run the application
    # In production, use gunicorn or uwsgi instead
    app.run(
        host=app.config.get('HOST', '0.0.0.0'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )
