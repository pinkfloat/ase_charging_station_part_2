# src/domain/aggregates/charging_station.py
import numpy as np
from domain.events.rating_added_event import RatingAddedEvent
from domain.entities.rating import Rating
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status
from domain.value_objects.rush_hours import RushHours

class ChargingStation:
    def __init__(self, station_id, name, operator, power, location, postal_code, status, rush_hour_data, event_publisher=None):
        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        if not isinstance(postal_code, PostalCode):
            raise TypeError("postal_code must be an instance of PostalCode")
        if not isinstance(status, Status):
            raise TypeError("status must be an instance of Status")
        if not isinstance(rush_hour_data, RushHours):
            raise TypeError("rush_hour_data must be an instance of RushHours")
        if not isinstance(power, (int, float)):
            raise TypeError("power must be a float or an int")
        if not isinstance(station_id, int):
            raise TypeError("station_id must be an int")

        self.station_id = station_id
        self.name = name
        self.operator = operator
        self.power = power
        self.location = location
        self.postal_code = postal_code
        self.status = status
        self.rush_hour_data = rush_hour_data
        self.ratings = []

        # Dependency injection for event publisher
        self.event_publisher = event_publisher or (lambda event: None)

    def publish_event(self, event):
        """Publishes an event using the injected publisher (i.e. flash)."""
        self.event_publisher(event)

    def add_rating(self, rating):
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.ratings.append(rating)

        # Create a RatingAddedEvent and publish it
        event = RatingAddedEvent(station_id=self.station_id, rating=rating)
        self.publish_event(event)

    def average_rating(self):
        if not self.ratings:
            return 0.0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)
