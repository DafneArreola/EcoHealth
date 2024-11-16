from flask_pymongo import PyMongo
from flask import current_app

def get_mongo():
    """Helper to access the MongoDB client."""
    return current_app.extensions['pymongo'].db

def insert_user(data):
    """Insert a new user into the database."""
    db = get_mongo()
    db.user_profiles.insert_one(data)

def find_user(username):
    """Find a user by username."""
    db = get_mongo()
    return db.user_profiles.find_one({"username": username})

# Add more helper functions as needed
