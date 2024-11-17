from flask_pymongo import PyMongo
from flask import current_app
from backend import mongo

def insert_user(data):
    """Insert a new user into the database."""
    mongo.db.user_profiles.insert_one(data)

def find_user(username):
    """Find a user by username."""
    user = mongo.db.user_profiles.find_one({"username": username})
    if user and "_id" in user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user

def update_user_field(username, field, value):
    """Update a specific field for a user."""
    result = mongo.db.user_profiles.update_one(
        {"username": username},
        {"$set": {field: value}}
    )
    return result.matched_count > 0  # Returns True if a document was updated

def get_user_with_nested_data(username):
    """Find a user by username."""
    user = mongo.db.user_profiles.find_one({"username": username})
    if user and "_id" in user:
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
    return user


def insert_environmental_data(username, environmental_data):
    """Insert or update environmental data for a user."""
    result = mongo.db.user_profiles.update_one(
        {"username": username},
        {"$set": {"environmental_data": environmental_data}}
    )
    return result.matched_count > 0

def insert_health_data(username, health_data):
    """Insert or update health data for a user."""
    result = mongo.db.user_profiles.update_one(
        {"username": username},
        {"$set": {"health_data": health_data}}
    )
    return result.matched_count > 0

def insert_health_subfield(username, subfield, data):
    """Insert or update a subfield in health data (e.g., sleep, wellness)."""
    result = mongo.db.user_profiles.update_one(
        {"username": username},
        {"$set": {f"health_data.{subfield}": data}}
    )
    return result.matched_count > 0
