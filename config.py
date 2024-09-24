import os
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object (this will be imported and initialized in app.py)
db = SQLAlchemy()

# Define a class to store configuration settings for the Flask app
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')  # Use an environment variable for extra security
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///tournament.db')  # Use environment variable for DB URI, fallback to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable SQLAlchemy event notifications (recommended for performance)
