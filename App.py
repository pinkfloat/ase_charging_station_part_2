from flask import Flask, render_template, request

# Create a Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to Berlin Charging Station"
@app.route('/index')
def index():
    return "<h1>Create a Customer Account</h1>"
@app.route('/form', methods = ["GET", "POST"])
def form():
    if request.method == "GET":
        return render_template("form.html")
#def Profile():
    #if request.method == "POST":
        #return render_template("CreateProfile.html")

if __name__ == "__main__":
    app.run(debug=False
    )