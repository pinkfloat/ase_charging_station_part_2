# charging_station/src/domain/aggregates/rated_charging_station.py
from charging_station.src.domain.events.rating_added_event import RatingAddedEvent
from charging_station.src.domain.entities.charging_station import ChargingStation
from charging_station.src.domain.entities.rating import Rating
from charging_station.src.domain.value_objects.location import Location
from charging_station.src.domain.value_objects.postal_code import PostalCode
from charging_station.src.domain.value_objects.status import Status
from charging_station.src.domain.value_objects.rush_hours import RushHours

class RatedChargingStation(ChargingStation):
    def __init__(self, station_id, name, operator, power, location, postal_code, status, rush_hour_data, event_publisher=None):
        """
        Initializes a RatedChargingStation aggregate.
        """
        super().__init__(station_id, name, operator, power)

        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        if not isinstance(postal_code, PostalCode):
            raise TypeError("postal_code must be an instance of PostalCode")
        if not isinstance(status, Status):
            raise TypeError("status must be an instance of Status")
        if not isinstance(rush_hour_data, RushHours):
            raise TypeError("rush_hour_data must be an instance of RushHours")

        self.location = location
        self.postal_code = postal_code
        self.status = status
        self.rush_hour_data = rush_hour_data
        self.ratings = []

        # Dependency Injection for Event-Publisher
        self.event_publisher = event_publisher or (lambda event: None)

    def publish_event(self, event):
        """
        Publishes an event using the injected event publisher.
        """
        self.event_publisher(event)

    def add_rating(self, rating):
        """
        Adds a rating to the station and publishes a RatingAddedEvent.
        """
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.ratings.append(rating)

        # Create a RatingAddedEvent and publish it
        event = RatingAddedEvent(rating)
        self.publish_event(event)

    def average_rating(self):
        """
        Calculates the average rating for the charging station.
        """
        if not self.ratings:
            return 0.0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)
