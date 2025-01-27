# src/domain/events/rating_added_event.py
from datetime import datetime
from domain.entities.rating import Rating

class RatingAddedEvent:
    def __init__(self, station_id, rating, timestamp=None):
        """Represents an event when a rating is added to a charging station."""
        if not isinstance(rating, Rating):
            raise TypeError("rating must be an instance of Rating")
        self.station_id = station_id
        self.rating = rating
        self.timestamp = timestamp or datetime.now().isoformat()

    def __repr__(self):
        return f"<RatingAddedEvent(station_id={self.station_id}, rating_value={self.rating.value}, timestamp={self.timestamp})>"
