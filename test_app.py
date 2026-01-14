"""
Simple test script to run the Flask app with SQLite
For quick local testing without MySQL
"""

# Temporarily replace the database module with SQLite version
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(__file__))

# Replace database module
import database_sqlite as database_module
sys.modules['database'] = database_module

# Now import and run the Flask app
from app import app, db

if __name__ == '__main__':
    print("="*60)
    print("🚀 Ryde University Student Records - Local Test Mode")
    print("="*60)
    print("📊 Using SQLite database (ryde_university.db)")
    print("🌐 Application will start at: http://localhost:5000")
    print("="*60)
    print()
    
    # Initialize database
    db.init_database()
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
