from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Response
from flask import Blueprint, request, jsonify, session
from backend.database import insert_user, find_user, update_user_field, get_user_with_nested_data, update_user

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


    session['user'] = username
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


@api.route('/complete_profile', methods=['POST'])
def complete_profile():
    data = request.json
    username = session.get('user')  # Ensure username is fetched from the session

    if not username:
        return jsonify({"success": False, "error": "User not logged in"}), 401

    # Prepare updates
    updates = {
        "age": int(data.get("age", 0)),
        "location": data.get("location"),
        "occupation": data.get("occupation"),
        "goals": data.get("goals", []),  # Already sent as a list
        "environmental_data": {
            "transportation": {
                "primary_mode": data.get("primary_mode"),
                "miles_per_day": int(data.get("miles_per_day", 0)),
                "public_transit": data.get("public_transit"),
                "bike_usage": data.get("bike_usage"),
                "walking": data.get("walking"),
                "flight_frequency": data.get("flight_frequency")
            },
            "diet": {
                "type": data.get("diet_type"),
                "local_food_percent": int(data.get("local_food_percent", 0)),
                "waste_frequency": data.get("waste_frequency"),
                "meal_planning": data.get("meal_planning") == "on",
                "composting": data.get("composting") == "on"
            }
        },
        "health_data": {
            "exercise": {
                "activity_level": data.get("activity_level"),
                "frequency": data.get("frequency"),
                "activities": data.get("activities", []),  # Already sent as a list
            },
            "sleep": {
                "average_hours": float(data.get("average_hours", 0)),
                "quality": data.get("quality"),
                "schedule": data.get("schedule")
            }
        }
    }

    # Update the user's profile
    update_user(username, updates)

    return jsonify({"success": True, "message": "Profile completed successfully!"})




