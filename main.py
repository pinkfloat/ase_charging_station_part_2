# Import standard libraries
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps

# Import domain services and repositories
from user.src.application.services.user_service import UserService
from user.src.infrastructure.repositories.user_repository import UserRepository

# Initialize Repositories and Services
user_repository = UserRepository(firebase_secret_json="./secret/firebase.json")
user_service = UserService(user_repository=user_repository)

# Initialize Firebase through repository (ensures single initialization)
user_repository.load_from_database()  # This triggers Firebase initialization

# Import custom application code
from dash_app import create_dash_app

# Initialize Application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used for flashing messages

# Initialize Dash app
create_dash_app(app) # Create and link the Dash app to the Flask app

# Authentication decorator using UserService
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        try:
            # Verify user exists through service
            user = user_service.user_repository.load_from_database()
            user_exists = any(u.id == session['user_id'] for u in user)
            if not user_exists:
                flash("Session invalid. Please login again.", "error")
                return redirect(url_for('logout'))
        except Exception as e:
            flash(f"Authentication error: {e}", "error")
            return redirect(url_for('logout'))
            
        return func(*args, **kwargs)
    return decorated_function

# Route to display the home page
@app.route("/")
def index():
    return render_template("index.html")

# Route to create a new user profile
@app.route("/create-profile", methods=["GET", "POST"])
def create_profile():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        try:
            user = user_service.create_user(username, password)
            flash(f"User {username} signed up successfully!", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e), "error")
        except Exception as e:
            flash(f"Error creating user: {e}", "error")
        
        return redirect(url_for("create_profile"))

    return render_template("CreateProfile_new.html")

# Route to handle user login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"].strip()

        try:
            users = user_service.get_all_users()
            for user in users:
                if user.name == username:
                    if user.password == user_repository.hash_password(password):
                        session['user_id'] = user.id
                        session['username'] = username
                        return redirect(url_for("dashboard"))
                    else:
                        flash("Incorrect password. Please try again.", "error")
                        return redirect(url_for("login"))
            
            flash("Username not found. Please sign up first.", "error")
            return redirect(url_for("create_profile"))
        except Exception as e:
            flash(f"Login error: {e}", "error")
            return redirect(url_for("login"))

    return render_template("LoginPage.html")

# Route to display the dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    """Redirects to the Dash app."""
    return redirect('/dashboard/')

# Route to handle user logout
@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
