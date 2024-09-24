from config import db  # Import db from config.py

# Admin model for storing admin user credentials
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(150), nullable=False, unique=True)  # Username must be unique
    password_hash = db.Column(db.String(128), nullable=False)  # Hashed password for security

# Athlete model for storing athlete details
class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    name = db.Column(db.String(150), nullable=False)  # Name of the athlete
    category = db.Column(db.String(100), nullable=False)  # Category (e.g., weight class)

# Match model for storing tournament match details
class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    athlete1_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=True)  # Foreign key referencing the first athlete
    athlete2_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=True)  # Foreign key referencing the second athlete
    score = db.Column(db.String(50))  # Match score
    winner = db.Column(db.String(150))  # Name of the winning athlete

    # Establish relationships to fetch athlete data easily
    athlete1 = db.relationship('Athlete', foreign_keys=[athlete1_id])
    athlete2 = db.relationship('Athlete', foreign_keys=[athlete2_id])
