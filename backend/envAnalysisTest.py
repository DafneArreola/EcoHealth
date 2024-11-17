import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import the app
from app import app

class TestEcoHealthAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Sample test data
        self.test_user_data = {
            "environmental_data": {
                "transportation": {
                    "miles_per_day": 50,
                    "primary_mode": "hybrid car"
                },
                "diet": {
                    "dietary_preferences": {
                        "red_meat": "low"
                    },
                    "local_food_percent": 60,
                    "waste_frequency": "rarely",
                    "composting": True
                },
                "consumption": {
                    "zero_waste_efforts": ["reusable bags", "water bottle"]
                }
            },
            "health_data": {
                "exercise": {
                    "frequency": "4-5 times per week",
                    "activities": ["yoga", "cycling"]
                }
            }
        }

    def test_environmental_impact_endpoint(self):
        """Test the /environmental_impact endpoint"""
        with patch('app.generate_chatgpt_response') as mock_chatgpt:
            # Mock ChatGPT response
            mock_chatgpt.return_value = "Sample ChatGPT response for environmental impact"
            
            # Make request to the endpoint
            response = self.app.post('/environmental_impact',
                                   data=json.dumps(self.test_user_data),
                                   content_type='application/json')
            
            # Check response
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            
            # Verify response structure
            self.assertIn('analysis', data)
            self.assertIn('co2_emissions', data['analysis'])
            self.assertIn('dietary_impact', data['analysis'])
            self.assertIn('waste_reduction_score', data['analysis'])
            self.assertIn('chatbot_response', data['analysis'])

if __name__ == '__main__':
    unittest.main()
    