from flask import Blueprint, request, jsonify, session
from backend.database import insert_user, find_user, update_user_field, get_user_with_nested_data

api = Blueprint("api", __name__)

@api.route("/register", methods=["POST"])
def register():
    data = request.json
    insert_user(data)
    return jsonify({"message": "User registered successfully!"})

@api.route("/login", methods=["POST"])
def login():
    data = request.json
    user = find_user(data.get("username"))
    if user:
        session["user"] = user["username"]
        return jsonify({"message": "Login successful!"})
    return jsonify({"error": "User not found"}), 404

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
