from flask import Flask, render_template

app = Flask(__name__, template_folder="frontend/templates", static_folder="frontend/static")
app.secret_key = " "

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

# Dashboard (or redirect after login)
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']}! <a href='/logout'>Logout</a>"
    return redirect(url_for('login'))

# Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
