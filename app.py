from datetime import datetime
from dash import Dash, dcc, html, Input, Output, State
from firebase_admin import credentials, initialize_app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import hashlib
import pandas as pd
import plotly.express as px


# Initialize Application
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Used for flashing messages


# Initialize Database
cred = credentials.Certificate("./secret/firebase.json")  # Make sure the secret key is placed here
initialize_app(cred, {
    'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'
})

########### plotly dash app starts from here ##############

# Initialize Dash app
dash_app = Dash(__name__, server=app, url_base_pathname='/dashboard/')

# Load charging station data from CSV file
df = pd.read_csv('./data/ChargingStationData.csv', usecols=['stationID','stationName', 'stationOperator', 'PLZ', 'Latitude', 'Longitude', 'KW'])
df['PLZ'] = df['PLZ'].astype(str)

# Define layout of the Dash app
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Interval(id='interval-component', interval=1000, n_intervals=0),

    html.Div([
        html.Span(f"Welcome, ", id='welcome-user'),
        html.Span(id='username-display', style={'fontWeight': 'bold'}),
    ], style={'position': 'absolute', 'top': '10px', 'left': '10px'}),

    html.H1("Charging Stations", style={'textAlign': 'center'}),
    html.A("Logout", href="/logout", style={'position': 'absolute', 'top': '10px', 'right': '10px'}),
    html.Div([
        html.Div([
            dcc.Input(
                id='plz-search',
                type='text',
                placeholder='Please enter the Pincode here...',
                style={'width': '400px', 'margin': '10px'}
            ),
            html.Button('Search', id='search-button', n_clicks=0),
            html.Div(id='search-message', style={'color': 'red', 'margin': '10px'}),
            dcc.Graph(id='station-map', style={'height': '80vh'})
        ], style={'flex': '75%', 'display': 'flex', 'flexDirection': 'column'}),
        
        html.Div([
        html.Div(id='station-details'),
        html.Div(id='average-rating'),
        html.Div(id='reviews-list'),
        html.Div([
            dcc.Slider(id='rating-slider', min=1, max=5, step=1, marks={i: str(i) for i in range(1, 6)}),
            dcc.Input(
                id='feedback-input',
                type='text',
                placeholder='Leave feedback...',
                style={'width': '100%', 'margin-bottom': '10px'}
            ),
            html.Button('Submit Feedback', id='submit-feedback', n_clicks=0)
        ], id='feedback-div', style={'display': 'none'}),
        html.Div(id='feedback-output')
    ], style={'flex': '25%', 'padding': '20px'})


    ], style={'display': 'flex'})
])

# Callback to update the username displayed in the app
@dash_app.callback(
    Output('username-display', 'children'),
    Input('interval-component', 'n_intervals')
)
def update_username(n):
    """Updates the displayed username."""
    return session.get('username', '')

# Callback to update the map based on the user's search for charging stations
@dash_app.callback(
    [Output('station-map', 'figure'),
     Output('search-message', 'children'),
     Output('plz-search', 'value')], 
    [Input('search-button', 'n_clicks'),
     Input('station-map', 'figure')],
    State('plz-search', 'value')
)
def update_map(n_clicks, current_figure, search_plz):
    """Filters the data based on the entered postal code and updates the map accordingly."""
    if not search_plz:
        filtered_df = df
        message = ""
    else:
        filtered_df = df[df['PLZ'] == search_plz]
        if filtered_df.empty:
            message = "No data found for the entered Pincode."
            return current_figure, message, ""  # Return empty string for search box
        else:
            message = ""

    fig = px.scatter_mapbox(
        filtered_df,
        lat='Latitude',
        lon='Longitude',
        hover_data=['stationID','stationName', 'stationOperator', 'KW', 'PLZ'],
        zoom=15 if search_plz else 10,
        mapbox_style="open-street-map"
    )
    
    fig.update_traces(marker=dict(size=15, symbol='circle') if search_plz else dict(size=8, symbol='circle'))
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    
    return fig, message, ""  # Return empty string for search box

# Callback to display charging station details and reviews when a station is clicked
@dash_app.callback(
    [Output('station-details', 'children'),
     Output('feedback-div', 'style'),
     Output('average-rating', 'children'),
     Output('reviews-list', 'children')],
    Input('station-map', 'clickData')
)
def display_station_details(click_data):
    """Displays the details of the clicked station, its average rating, and any reviews."""
    if click_data:
        point_data = click_data['points'][0]
        station_id = point_data['customdata'][0]  # Get station ID from clicked data
        
        # Fetch reviews for the selected station from the database
        ratings_ref = db.reference('ratings')
        all_reviews = ratings_ref.get() or {}
        station_reviews = [review for review in all_reviews.values() if review['charging_station_id'] == station_id]
        
        # Calculate the average rating
        if station_reviews:
            avg_rating = sum(review['review_star'] for review in station_reviews) / len(station_reviews)
        else:
            avg_rating = 0
        
        # Prepare list of reviews to display
        reviews_list = [html.P(f"{review['review_text']} (Rating: {review['review_star']})") for review in station_reviews]
        
        return (
            html.Div([
                html.H3("Station Details"),
                html.P(f"Name: {point_data['customdata'][1]}"),
                html.P(f"Operator: {point_data['customdata'][2]}"),
                html.P(f"Power: {point_data['customdata'][3]} KW"),
                html.P(f"PLZ: {point_data['customdata'][4]}"),
            ]),
            {'display': 'block'},
            html.H4(f"Average Rating: {avg_rating:.2f}"),
            html.Div(reviews_list)
        )
    else:
        return (
            html.Div([
                html.H3("Charging Stations"),
                html.P(f"There are {len(df)} charging stations in total."),
                html.P("Please click on a station to view its details and leave a review.")
            ]),
            {'display': 'none'},
            '',
            ''
        )

# Callback to handle the submission of feedback and ratings for a station
@dash_app.callback(
    [Output('feedback-output', 'children'),
     Output('feedback-input', 'value'),
     Output('rating-slider', 'value')],
    [Input('submit-feedback', 'n_clicks'),
     Input('station-map', 'clickData')],
    [State('feedback-input', 'value'),
     State('rating-slider', 'value')]
)
def submit_feedback(n_clicks, click_data, feedback, rating):
    """Submits the feedback and rating for the selected station and stores it in the database."""
    if n_clicks > 0 and feedback and rating and click_data:
        user_id = session.get('user_id')
        if not user_id:
            return "You need to log in to give a rating.", "", None
        
        station_id = click_data['points'][0]['customdata'][0]  # Get station ID from clicked data
        
        try:
            # Store the feedback in the Firebase database
            ratings_ref = db.reference('ratings')
            ratings_ref.push({
                "user_id": user_id,
                "charging_station_id": station_id,
                "review_star": rating,
                "review_text": feedback,
                "review_date": datetime.now().isoformat()
            })
            return "Thank you for your review!", "", None
        except Exception as e:
            return f"Error adding review: {e}", feedback, rating
    
    return "", "", None

###########  plotly dash app ends here ##############

# Decorator to require login before accessing certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

# Route to handle user logout
@app.route("/logout")
def logout():
    """Logs the user out by removing user session data."""
    session.pop('user_id', None)
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# Route to display the dashboard
@app.route("/dashboard")
@login_required
def dashboard():
    """Renders the dashboard page, which is protected by login."""
    return dash_app.index()

if __name__ == "__main__":
    app.run(debug=True)
