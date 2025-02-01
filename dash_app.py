from dash import Dash, dcc, html, Input, Output, State
from datetime import datetime
from enum import Enum
from flask import session
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from charging_station.src.application.services.charging_station_service import ChargingStationService
from charging_station.src.infrastructure.repositories.rated_charging_station_repository import RatedChargingStationRepository

def create_dash_app(flask_app):
    dash_app = Dash(__name__, server=flask_app, 
                   url_base_pathname='/dashboard/', 
                   suppress_callback_exceptions=True)

    # Initialize repositories and services
    station_repository = RatedChargingStationRepository(firebase_secret_json="./secret/firebase.json")
    station_service = ChargingStationService(repository=station_repository)

    # Load initial data
    try:
        station_service.load_stations_from_csv('bounded_contexts/charging_station/src/infrastructure/data/ChargingStationData.csv')
                                        
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
    @dash_app.callback(
        Output('username-display', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def update_username(n):
        return session.get('username', '')

    @dash_app.callback(
        [Output('station-map', 'figure'),
         Output('search-message', 'children'),
         Output('plz-search', 'value')],
        [Input('search-button', 'n_clicks'),
         Input('station-map', 'figure')],
        State('plz-search', 'value')
    )
    def update_map(n_clicks, current_figure, search_plz):
        if not search_plz:
            filtered_df = df
            message = ""
        else:
            filtered_df = df[df['PLZ'] == search_plz]
            if filtered_df.empty:
                message = "No data found for the entered Pincode."
                return current_figure, message, ""
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
        fig.update_traces(marker=dict(size=15 if search_plz else 8, symbol='circle'))
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
        
        return fig, message, ""

    @dash_app.callback(
        [Output('station-details', 'children'),
         Output('status', 'children'),
         Output('feedback-div', 'style'),
         Output('average-rating', 'children'),
         Output('reviews-list', 'children')],
        Input('station-map', 'clickData')
    )
    def display_station_details(click_data):
        if click_data:
            station_id = click_data['points'][0]['customdata'][0]
            
            try:
                # Find station using domain service
                station = next(s for s in station_service.repository.stations 
                             if s.station_id == station_id)
                
                # Calculate average rating from domain entity
                avg_rating = station.average_rating()
                
                # Generate status using domain value object
                random_status = station.status
                
                # Generate rush hours data
                rush_data = station.rush_hour_data
                
                # Create details components
                details = html.Div([
                    html.H3("Station Details"),
                    html.P(f"Name: {station.name}"),
                    html.P(f"Operator: {station.operator}"),
                    html.P(f"Power: {station.power} KW"),
                    html.P(f"PLZ: {station.postal_code.plz}"),         
                ])

                # Create status components
                status_display = html.Div([
                    html.H4(f"Status: {random_status.value}"),
                    dcc.Graph(
                        figure=go.Figure(
                            data=[go.Bar(x=rush_data.time_slots, 
                                       y=rush_data.data,
                                       marker_color='skyblue')],
                            layout=go.Layout(
                                title='Simulated Rush Hour Data',
                                xaxis_title='Time of Day',
                                yaxis_title='Persons per Hour',
                                template='plotly_white'
                            )
                        )
                    )
                ])

                # Create reviews list
                reviews = [html.P(f"{rating.comment} (Rating: {rating.value})") 
                         for rating in station.ratings]

                return (
                    details,
                    status_display,
                    {'display': 'block'},
                    html.H4(f"Average Rating: {avg_rating:.2f}"),
                    html.Div(reviews)
                )

            except StopIteration:
                pass  # Handle station not found

        # Default return when no station selected
        default_content = html.Div([
            html.H3("Charging Stations"),
            html.P(f"There are {len(df)} charging stations in total."),
            html.P("Please click on a station to view its details and leave a review.")
        ])
        return (
            default_content,
            '',
            {'display': 'none'},
            '',
            ''
        )

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
        if not rating:
            return "Please select a score", "", None
        if n_clicks > 0 and click_data and feedback:
            user_id = session.get('user_id')
            if not user_id:
                return "You need to log in to give a rating.", "", None

            station_id = click_data['points'][0]['customdata'][0]
            print('Goodby cruel world')
            try:
                station_service.add_rating_to_station(
                    user_id=user_id,
                    station_id=int(station_id),
                    value=rating,
                    comment=feedback
                )
                return "Thank you for your review!", "", None
            except Exception as e:
                return f"Error submitting review: {e}", feedback, rating

        return "", "", None

    return dash_app
