from flask import Flask

# Create a Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Berlin Charging Station"
@app.route('/index')
def index():
    return "<h1>Create a Customer Account</h1>"

if __name__ == "__main__":
    app.run(debug=True)