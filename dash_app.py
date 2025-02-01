from dash import Dash, dcc, html, Input, Output, State
from datetime import datetime
from enum import Enum
from flask import session
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

from bounded_contexts.charging_station.src.application.services.charging_station_service import ChargingStationService
from bounded_contexts.charging_station.src.infrastructure.repositories.rated_charging_station_repository import RatedChargingStationRepository
from bounded_contexts.charging_station.src.domain.value_objects.status import Status
from bounded_contexts.charging_station.src.domain.value_objects.rush_hours import RushHours


def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, 
                   url_base_pathname='/dashboard/', 
                   suppress_callback_exceptions=True)

    # Initialize repositories and services
    station_repository = RatedChargingStationRepository(firebase_secret_json="./secret/firebase.json")
    station_service = ChargingStationService(repository=station_repository)

    # Load initial data
    try:
        station_service.load_stations_from_csv(r'bounded_contexts\charging_station\src\infrastructure\data\ChargingStationData.csv')
                                        
        station_service.load_all_ratings_to_stations()
    except Exception as e:
        print(f"Error loading station data: {e}")

    # Create DataFrame for mapping
    stations = station_repository.stations
    df = pd.DataFrame([{
        'stationID': s.station_id,
        'stationName': s.name,
        'stationOperator': s.operator,
        'KW': s.power,
        'Latitude': s.location.latitude,
        'Longitude': s.location.longitude,
        'PLZ': s.postal_code.plz
    } for s in stations])

    # Layout

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Interval(id='interval-component', interval=1000, n_intervals=0),

        # Show start welcoming text
        # The user will have the options to login or create a profile from here
        html.Div([
            html.Span(f"Welcome, ", id='welcome-user'),
            html.Span(id='username-display', style={'fontWeight': 'bold'}),
        ], style={'position': 'absolute', 'top': '10px', 'left': '10px'}),

        # The screen after login
        html.H1("Charging Stations", style={'textAlign': 'center'}),
        html.A("Logout", href="/logout", style={'position': 'absolute', 'top': '10px', 'right': '10px'}),
        html.Div([
            # The charging station search bar (on the top left part of the page)
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
            
            # If a charging station marker is clicked, the station details are shown
            html.Div([
                html.Div(id='station-details'),
                html.Div(id='status'),
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

    # Callbacks

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
        Output('status', 'children'),
        Output('feedback-div', 'style'),
        Output('average-rating', 'children'),
        Output('reviews-list', 'children')],
        Input('station-map', 'clickData')
    )
    def display_station_details(dataOfClickedStation):
        """
        Displays the details of the clicked station, its average rating, and any reviews.
        """

        def calculate_average_rating(station_reviews):
            """Calculate the average rating based on a list of reviews."""
            if station_reviews:
                avg_rating = sum(review['review_star'] for review in station_reviews) / len(station_reviews)
            else:
                avg_rating = 0.0
            return avg_rating
        
        def simulate_station_availability():
            class Status(Enum):
                AVAILABLE = "available"
                OCCUPIED = "occupied"
                OUT_OF_SERVICE = "out of service"
                MAINTENANCE = "maintenance"
            random_status = random.choice(list(Status))
            return random_status
        
        def simulate_rush_hours():
            time_slots = ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM"]
            random_data = np.random.normal(loc=2.5, scale=1.0, size=len(time_slots))
            random_data = np.clip(random_data, 0, 5) # simulate 0-5 persons per hour
            bar_chart = go.Figure(data=[go.Bar(x=time_slots, y=random_data, marker_color='skyblue')])
            bar_chart.update_layout(
                title='Simulated rush hour data',
                xaxis_title='Time of Day',
                yaxis_title='Persons per Hour',
                template='plotly_white'
            )
            return bar_chart

        if dataOfClickedStation:
            point_data = dataOfClickedStation['points'][0]
            station_id = point_data['customdata'][0]  # Get station ID from clicked data
            
            # Fetch reviews for the selected station from the database
            ratings_ref = db.reference('ratings')
            all_reviews = ratings_ref.get() or {}
            station_reviews = [review for review in all_reviews.values() if review['charging_station_id'] == station_id]
            
            # Prepare list of reviews to display
            reviews_list = [html.P(f"{review['review_text']} (Rating: {review['review_star']})") for review in station_reviews]

            # Display average rating, station availability and simulated rush hours
            avg_rating = calculate_average_rating(station_reviews)
            random_status = simulate_station_availability()
            bar_chart = simulate_rush_hours()
            
            return (
                html.Div([
                    html.H3("Station Details"),
                    html.P(f"Name: {point_data['customdata'][1]}"),
                    html.P(f"Operator: {point_data['customdata'][2]}"),
                    html.P(f"Power: {point_data['customdata'][3]} KW"),
                    html.P(f"PLZ: {point_data['customdata'][4]}"),
                ]),
                html.Div([
                    html.H4(f"Status: {random_status.value}"),
                    dcc.Graph(figure=bar_chart, style={'height': '300px'})
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
                '', # no status
                {'display': 'none'},
                '', # no rating
                ''  # no reviews
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
    def submit_feedback(n_clicks, dataOfClickedStation, feedback, rating):
        """Submits the feedback and rating for the selected station and stores it in the database."""
        if n_clicks > 0 and feedback and rating and dataOfClickedStation:
            user_id = session.get('user_id')
            if not user_id:
                return "You need to log in to give a rating.", "", None
            
            station_id = dataOfClickedStation['points'][0]['customdata'][0]
            
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
