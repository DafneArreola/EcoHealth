from envImpact import EnvironmentalImpact

def test_quick_insights():
    """Test quick environmental impact insights"""
    
    # Initialize analyzer
    analyzer = EnvironmentalImpact()
    
    # Test single data points
    print("\nTesting single data point insights:")
    print("-" * 50)
    
    # Test flight frequency
    flight_data = {"flight_frequency": "quarterly for work"}
    print(f"\nFlight data: {flight_data}")
    print(f"Impact: {analyzer.get_quick_insight(flight_data)}")
    
    # Test local food
    food_data = {"local_food_percent": 60}
    print(f"\nLocal food data: {food_data}")
    print(f"Impact: {analyzer.get_quick_insight(food_data)}")
    
    # Test multiple data points
    print("\nTesting multiple data points insight:")
    print("-" * 50)
    
    # Combine transportation and consumption
    multi_data = {
        "transportation": {
            "primary_mode": "hybrid car",
            "miles_per_day": 120
        },
        "consumption": {
            "zero_waste_efforts": ["reusable bags", "water bottle"]
        }
    }
    print(f"\nMultiple data points: {multi_data}")
    print(f"Combined Impact: {analyzer.get_multi_point_insight(multi_data)}")

if __name__ == "__main__":
    test_quick_insights()