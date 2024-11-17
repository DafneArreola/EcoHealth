from flask import render_template, session, redirect, url_for, request
from backend import create_app
from backend.routes import api

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
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Replace this with your user authentication logic
        username = request.form['username']
        password = request.form['password']
        
        # Dummy credentials for demonstration
        if username == 'admin' and password == 'password':
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid username or password")
    
    return render_template('login.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # Pass the mock twin state to the template
        return render_template('dashboard.html', 
                             username=session['user'],
                             twin_state=mock_twin_state)
    return redirect(url_for('login'))

# Logout Page
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Capture form data
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        # Check if user already exists
        mongo = app.extensions['pymongo'].db
        existing_user = mongo.users.find_one({"username": username})
        if existing_user:
            return render_template('register.html', error="Username already exists")

        # Add user to the database
        mongo.users.insert_one({
            "username": username,
            "password": password,  # NOTE: Use password hashing in production
            "email": email
        })
        return redirect(url_for('login'))

    return render_template('register.html')

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
