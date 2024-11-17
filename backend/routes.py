from flask import Blueprint, request, jsonify, session
from backend.database import insert_user, find_user

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
