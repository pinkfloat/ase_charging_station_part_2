from flask import Flask, render_template, request

# Create a Flask application
app = Flask(__name__)

known_user = {
    "admin": "1234" # Example: Username: "admin", Password: "1234"
}

@app.route('/')
def home():
    return "Welcome to Berlin Charging Station"

@app.route('/index')
def index():
    return "<h1>Create a Customer Account</h1>"

@app.route('/login', methods = ["GET", "POST"])
def login():
    if request.method == "POST":
        # Handle form submission
        username = request.form['username']
        password = request.form['password']

        # Validate username and password
        if username in known_user and known_user[username] == password:
            # Login successful
            return f"Welcome, {username}! You are logged in."
        else: # Login failed
            return "Invalid username or password. Please try again."

    else: #if request.method == "GET":
        return render_template("LoginPage.html")

#def Profile():
    #if request.method == "POST":
        #return render_template("CreateProfile.html")

if __name__ == "__main__":
    app.run(debug=False)