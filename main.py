# Import standard libraries
from datetime import datetime
from firebase_admin import credentials, initialize_app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import hashlib

# Import custom application code
from dash_app import create_dash_app

# Initialize Application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used for flashing messages

# Initialize Database
cred = credentials.Certificate("./secret/firebase.json")  # Make sure the secret key is placed here
initialize_app(cred, {
    'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'
})

# Initialize Dash app
create_dash_app(app) # Create and link the Dash app to the Flask app

# Function to hash passwords for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Route to display the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route to create a new user profile
@app.route("/create-profile", methods=["GET", "POST"])
def create_profile():
    """Handles the creation of a new user profile, including username and password."""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        hashed_password = hash_password(password)

        try:
            users_ref = db.reference("users")
            users = users_ref.get() or {}
            
            # Check if username already exists
            for user_id, user_data in users.items():
                if user_data["username"] == username:
                    flash("Username already exists. Please choose another.", "error")
                    return redirect(url_for("create_profile"))

            # Create new user
            user_id = f"user_{len(users) + 1}"
            users_ref.child(user_id).set({
                "username": username,
                "password": hashed_password,
                "date_joined": datetime.now().isoformat()
            })
            flash(f"User {username} signed up successfully!", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash(f"Error signing up: {e}", "error")
            return redirect(url_for("create_profile"))

    return render_template("CreateProfile.html")

# Route to handle user login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Handles user login, verifying username and password."""
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()
        hashed_password = hash_password(password)

        try:
            users_ref = db.reference("users")
            users = users_ref.get() or {}
            
            for user_id, user_data in users.items():
                if user_data["username"] == username:
                    if user_data["password"] == hashed_password:
                        session['user_id'] = user_id
                        session['username'] = username  # Store username in session
                        return redirect(url_for("dashboard"))
                    else:
                        flash("Incorrect password. Please try again.", "error")
                        return redirect(url_for("login"))
            
            flash("Username not found. Please sign up first.", "error")
            return redirect(url_for("create_profile"))
        except Exception as e:
            flash(f"Error logging in: {e}", "error")
            return redirect(url_for("login"))

    return render_template("LoginPage.html")

# Decorator to require login before allowing access to dashboard
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function

# Route to display the dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    """Redirects to the Dash app."""
    return redirect('/dashboard/')

# Route to handle user logout
@app.route("/logout")
def logout():
    """Logs the user out by removing user session data."""
    session.pop('user_id', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
