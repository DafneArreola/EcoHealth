from flask import Flask
from flask_pymongo import PyMongo

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/ecohealth_database"

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.secret_key = "m8RnxOEE8y5VQmnE"
    
    # Configure MongoDB
    app.config["MONGO_URI"] = MONGO_URI
    mongo = PyMongo(app)
    
    # Register routes
    from backend.routes import api
    app.register_blueprint(api, url_prefix="/api")
    
    return app
