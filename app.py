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
