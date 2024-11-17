from flask import Flask
from flask_pymongo import PyMongo

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/ecohealth_database"

mongo = PyMongo()

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.secret_key = "m8RnxOEE8y5VQmnE"
    
    # Configure MongoDB
    app.config["MONGO_URI"] = MONGO_URI
    mongo.init_app(app)

    # # Ensure the users collection exists
    # db = mongo.db
    # if "users" not in db.list_collection_names():
    #     db.create_collection("users")
    
    # Register routes
    from backend.routes import api
    app.register_blueprint(api, url_prefix="/api")
    
    return app
