from poc import DigitalTwin
import json

def test_initial_state():
    """Test creating and initializing a Digital Twin"""
    twin = DigitalTwin("test_user")
    print("\nTest 1 - Initial State:")
    print(json.dumps(twin.current_state, indent=2))

def test_update_with_minimal_data():
    """Test updating with minimal data"""
    twin = DigitalTwin("test_user")
    minimal_data = {
        "environmental": {
            "transportation": {
                "primary_mode": "hybrid car",
                "miles_per_day": 30
            }
        },
        "health": {
            "sleep": {
                "average_hours": 8,
                "quality": "good"
            }
        }
    }
    
    print("\nTest 2 - Minimal Data Update:")
    result = twin.update_state(minimal_data)
    print(json.dumps(result, indent=2))

def test_jessica_scenario():
    """Test full Jessica scenario"""
    jessica_twin = DigitalTwin("jessica_chen")
    
    # Jessica's initial data
    initial_data = {
        "environmental": {
            "transportation": {
                "primary_mode": "hybrid car",
                "miles_per_day": 120,
                "public_transit": "0 times per week"
            },
            "diet": {
                "type": "unrestricted",
                "local_food_percent": 60,
                "composting": True
            },
            "consumption": {
                "packaging": "prefers minimal",
                "repair_habits": "tries to repair before replacing",
                "zero_waste_efforts": ["reusable bags", "water bottle"]
            }
        },
        "health": {
            "exercise": {
                "frequency": "4-5 times per week",
                "activities": ["yoga", "cycling", "hiking"],
                "average_duration": 45
            },
            "sleep": {
                "average_hours": 7.5,
                "quality": "good"
            },
            "wellness": {
                "stress_level": "moderate"
            }
        }
    }
    
    print("\nTest 3 - Jessica's Initial State:")
    result = jessica_twin.update_state(initial_data)
    print(json.dumps(result, indent=2))
    
    # Test scenario simulation
    scenario = {
        "changes": [
            {
                "type": "transportation",
                "change": "increase public transit to 3 times/week",
                "timeline": "1 month"
            },
            {
                "type": "diet",
                "change": "cut out red40 and other artificial dyes",
                "timeline": "2 weeks"
            }
        ]
    }
    
    print("\nTest 4 - Jessica's Simulation Results:")
    simulation = jessica_twin.simulate_scenario(scenario)
    print(json.dumps(simulation, indent=2))
    
def test_smart_recommendations():
    """Test getting smart recommendations"""
    jessica_twin = DigitalTwin("jessica_chen")

    # Jessica's initial data (define it here or move it to global scope)
    initial_data = {
        "environmental": {
            "transportation": {
                "primary_mode": "hybrid car",
                "miles_per_day": 120,
                "public_transit": "0 times per week"
            },
            "diet": {
                "type": "unrestricted",
                "local_food_percent": 60,
                "composting": True
            },
            "consumption": {
                "packaging": "prefers minimal",
                "repair_habits": "tries to repair before replacing",
                "zero_waste_efforts": ["reusable bags", "water bottle"]
            }
        },
        "health": {
            "exercise": {
                "frequency": "4-5 times per week",
                "activities": ["yoga", "cycling", "hiking"],
                "average_duration": 45
            },
            "sleep": {
                "average_hours": 7.5,
                "quality": "good"
            },
            "wellness": {
                "stress_level": "moderate"
            }
        }
    }

    # First update with initial data
    result = jessica_twin.update_state(initial_data)

    # Get smart recommendations
    recommendations = jessica_twin.get_smart_recommendations()

    print("\nTest 5 - Jessica's Smart Recommendations:")
    print(json.dumps(recommendations, indent=3))

if __name__ == "__main__":
    # Run all tests
    test_initial_state()
    test_update_with_minimal_data()
    test_jessica_scenario()
    test_smart_recommendations()