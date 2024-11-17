from flask import Flask
from flask_pymongo import PyMongo

# Initialize Flask app and MongoDB connection
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/ecohealth_database"
mongo = PyMongo(app)

def create_collections():
    """Set up the user_profiles collection with nested subtables."""
    db = mongo.db

    # User Profiles Collection
    db.create_collection("user_profiles", validator={
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "age", "location", "occupation", "goals"],
            "properties": {
                "username": {"bsonType": "string"},
                "age": {"bsonType": "int"},
                "location": {"bsonType": "string"},
                "occupation": {"bsonType": "string"},
                "goals": {"bsonType": "array", "items": {"bsonType": "string"}},

                # Environmental Data as a nested field
                "environmental_data": {
                    "bsonType": "object",
                    "properties": {
                        "transportation": {
                            "bsonType": "object",
                            "properties": {
                                "primary_mode": {"bsonType": "string"},
                                "miles_per_day": {"bsonType": "int"},
                                "public_transit": {"bsonType": "string"},
                                "bike_usage": {"bsonType": "string"},
                                "walking": {"bsonType": "string"},
                                "flight_frequency": {"bsonType": "string"}
                            }
                        },
                        "diet": {
                            "bsonType": "object",
                            "properties": {
                                "type": {"bsonType": "string"},
                                "local_food_percent": {"bsonType": "int"},
                                "waste_frequency": {"bsonType": "string"},
                                "meal_planning": {"bsonType": "bool"},
                                "composting": {"bsonType": "bool"},
                                "shopping_habits": {
                                    "bsonType": "object",
                                    "properties": {
                                        "bulk_buying": {"bsonType": "bool"},
                                        "farmers_market": {"bsonType": "string"},
                                        "organic_preference": {"bsonType": "string"},
                                        "seasonal_produce": {"bsonType": "string"}
                                    }
                                }
                            }
                        },
                        "consumption": {
                            "bsonType": "object",
                            "properties": {
                                "packaging": {"bsonType": "string"},
                                "repair_habits": {"bsonType": "string"},
                                "second_hand": {"bsonType": "string"},
                                "zero_waste_efforts": {"bsonType": "array", "items": {"bsonType": "string"}}
                            }
                        }
                    }
                },

                # Health Data as a nested field
                "health_data": {
                    "bsonType": "object",
                    "properties": {
                        "exercise": {
                            "bsonType": "object",
                            "properties": {
                                "activity_level": {"bsonType": "string"},
                                "frequency": {"bsonType": "string"},
                                "activities": {"bsonType": "array", "items": {"bsonType": "string"}},
                                "average_duration": {"bsonType": "int"}
                            }
                        },
                        "sleep": {
                            "bsonType": "object",
                            "properties": {
                                "average_hours": {"bsonType": "double"},
                                "quality": {"bsonType": "string"},
                                "schedule": {"bsonType": "string"}
                            }
                        },
                        "wellness": {
                            "bsonType": "object",
                            "properties": {
                                "stress_level": {"bsonType": "string"},
                                "activities": {"bsonType": "array", "items": {"bsonType": "string"}}
                            }
                        }
                    }
                }
            }
        }
    })

    print("User profiles collection with nested subtables created successfully!")

if __name__ == "__main__":
    with app.app_context():
        create_collections()