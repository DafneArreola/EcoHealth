from flask import render_template, session, redirect, url_for, request
from backend import create_app
from backend.routes import api

# Initialize Flask app using create_app
app = create_app()
#app.register_blueprint(api, url_prefix="/api")

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


@app.route('/test')
def test_page():
    return render_template('test_page.html')

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
