from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Response
from flask import Blueprint, request, jsonify, session
from backend.database import insert_user, find_user, update_user_field, get_user_with_nested_data

api = Blueprint("api", __name__)

@api.route('/register', methods=['POST'])
def register():
    data = request.json  # Ensure JSON data is sent
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Check if the user already exists
    if find_user(username):
        return jsonify({"success": False, "error": "Username already exists!"}), 400

    # Insert the new user
    insert_user({
        "username": username,
        "password": password,  # Add password hashing for production
        "email": email
    })
    return jsonify({"success": True, "message": "Registration successful! Please login."}), 200

@api.route('/login', methods=['POST'])
def login():
    data = request.json  # Ensure JSON data is sent
    username = data.get('username')
    password = data.get('password')

    # Check if the user exists
    user = find_user(username)
    if not user or user['password'] != password:  # Use hashed password verification in production
        return jsonify({"success": False, "error": "Invalid username or password!"}), 401

    # Set user in session
    session['user'] = user['username']
    return jsonify({"success": True, "message": "Login successful!"}), 200

@api.route("/user/<username>", methods=["GET"])
def get_user(username):
    user = get_user_with_nested_data(username)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

@api.route("/user/<username>/environmental_data", methods=["PUT"])
def update_environmental_data(username):
    data = request.json
    success = update_user_field(username, "environmental_data", data)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Environmental data updated successfully"})

@api.route("/user/<username>/health_data", methods=["PUT"])
def update_health_data(username):
    data = request.json
    success = update_user_field(username, "health_data", data)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Health data updated successfully"})

@api.route("/user/<username>/health_data/sleep", methods=["PUT"])
def update_sleep_data(username):
    data = request.json
    success = update_user_field(username, "health_data.sleep", data)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Sleep data updated successfully"})

@api.route("/user/<username>/health_data/wellness", methods=["PUT"])
def update_wellness_data(username):
    data = request.json
    success = update_user_field(username, "health_data.wellness", data)
    if not success:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"message": "Wellness data updated successfully"})
