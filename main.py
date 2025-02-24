# main.py
from infrastructure.api import app
from infrastructure.database import create_tables

if __name__ == '__main__':
    # Initialize database tables
    create_tables()
    # Run the Flask application
    app.run(host='0.0.0.0', port=5001, debug=True)