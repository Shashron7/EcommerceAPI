# The __init__.py file has several important roles:

# It marks the app directory as a Python package
# Creates the global database object
# Contains the create_app() function which:

# Creates a new Flask application
# Sets up configuration (database URI, secret key, etc.)
# Initializes extensions (like SQLAlchemy)
# Registers routes
# Creates database tables
# Returns the configured app


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy instance - this should be the ONLY instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize db with app
    db.init_app(app)
    
    # Import routes after db initialization to avoid circular imports
    from app.routes import initialize_routes
    initialize_routes(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app