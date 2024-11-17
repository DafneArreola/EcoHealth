from flask import render_template, session, redirect, url_for, request, jsonify
from backend import create_app
from backend.routes import api
from backend.poc import DigitalTwin
from backend.database import find_user
from openai import OpenAI
import base64

# Initialize Flask app using create_app
app = create_app()
#app.register_blueprint(api, url_prefix="/api")

mock_twin_state = {
    'environmental': {
        'transportation': {'score': 65, 'key_factors': ['Uses hybrid vehicle', 'High daily mileage']},
        'diet': {'score': 70, 'key_factors': ['60% local food', 'Moderate meat consumption']},
        'consumption': {'score': 75, 'key_factors': ['Minimal packaging', 'Regular recycling']},
        'overall_score': 70
    },
    'health': {
        'exercise': {'score': 85, 'key_factors': ['Regular activity', 'Diverse exercises']},
        'sleep': {'score': 80, 'key_factors': ['Good sleep quality', '7.5 hours average']},
        'wellness': {'score': 75, 'key_factors': ['Moderate stress', 'Regular meditation']},
        'overall_score': 80
    },
    'carbon_footprint': 8.5,
    'combined_score': 75
}

# Home Page
@app.route('/')
def home():
    return render_template('home.html')

# Login Page
@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

# Handle redirection after successful login
@app.route('/redirect-after-login', methods=['GET'])
def redirect_after_login():
    return redirect(url_for('dashboard'))

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    
    # For admin user, use mock data
    if username == 'admin':
        return render_template('dashboard.html', 
                             username=username,
                             twin_state=mock_twin_state)
    
    # For other users, create new Digital Twin with default state
    twin = DigitalTwin(username)
    return render_template('dashboard.html', 
                         username=username,
                         twin_state=twin.current_state)

# API endpoint for Digital Twin simulation
@app.route('/api/simulate', methods=['POST'])
def simulate_changes():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        username = session['user']
        changes = request.json
        
        if username == 'admin':
            # For admin user, initialize with mock state
            twin = DigitalTwin(username)
            mock_data = {
                "environmental": {
                    "transportation": {
                        "primary_mode": "hybrid car",
                        "miles_per_day": 30,
                        "public_transit": "2 times per week"
                    },
                    "diet": {
                        "type": "unrestricted",
                        "local_food_percent": 60,
                        "composting": True
                    },
                    "consumption": {
                        "packaging": "minimal",
                        "repair_habits": "tries to repair",
                        "zero_waste_efforts": ["reusable bags", "water bottle"]
                    }
                },
                "health": {
                    "exercise": {
                        "frequency": "3-4 times per week",
                        "activities": ["running", "yoga"],
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
            twin.update_state(mock_data)
        else:
            # For other users, get their current data
            twin = DigitalTwin(username)
            user_data = find_user(username)
            if user_data:
                update_data = {
                    'environmental': user_data.get('environmental_data', {}),
                    'health': user_data.get('health_data', {})
                }
                twin.update_state(update_data)
        
        # Run actual simulation using DigitalTwin class
        result = twin.simulate_scenario(changes)
        
        if result['status'] == 'success':
            return jsonify(result)
        else:
            app.logger.error(f"Simulation failed: {result.get('message')}")
            return jsonify({'error': result.get('message')}), 500
            
    except Exception as e:
        app.logger.error(f"Simulation error: {str(e)}")
        return jsonify({'error': 'Failed to run simulation'}), 500

# API endpoint for recommendations
@app.route('/api/recommendations')
def get_recommendations():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    username = session['user']
    twin = DigitalTwin(username)
    
    # Get recommendations
    recommendations = twin.get_smart_recommendations()
    return jsonify(recommendations)

@app.route('/api/analyze-wellness', methods=['POST'])
def analyze_wellness():
    if 'user' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    try:
        # Get the image data
        data = request.json
        image_data = data['image'].split(',')[1]  # Remove the data URL prefix
        
        # Initialize OpenAI client
        client = OpenAI()
        
        # Prepare the system message for GPT-4 Vision
        system_message = """You are a concise wellness advisor focused on non-superficial health analysis. 
        Analyze the image for signs of health-related factors like:
        - Sleep quality (eye bags, tiredness)
        - Stress indicators
        - Hydration levels
        - General energy levels
        - Mention what is visible in the image and how it relates to health.
        
        Provide practical, health-focused recommendations. DO NOT comment on appearance or cosmetic factors.
        Focus on lifestyle and wellness improvements. Be concise and informative. No more than a few sentences."""
        
        # Call GPT-4 Vision API with the updated model name
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Updated model name
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Please analyze this image for health indicators and provide wellness recommendations. Focus on lifestyle factors, not appearance."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=500
        )
        
        analysis = response.choices[0].message.content
        
        return jsonify({
            'status': 'success',
            'analysis': analysis
        })
        
    except Exception as e:
        print(f"Error in wellness analysis: {str(e)}")
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# Logout Page
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


# Registration Page
@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')

# Handle redirection after successful registration
@app.route('/redirect-after-register', methods=['GET'])
def redirect_after_register():
    return redirect(url_for('login_page'))

# Forgot Password Page
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        # Dummy response for demonstration
        return render_template('forgot_password.html', message="Check your email for reset instructions.")
    return render_template('forgot_password.html')


@app.route('/test')
def test_page():
    return render_template('test_page.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
