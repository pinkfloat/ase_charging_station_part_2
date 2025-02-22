# charging_station/src/domain/events/rating_added_event.py
from charging_station.src.domain.entities.rating import Rating

class RatingAddedEvent:
    def __init__(self, rating: Rating) -> None:
        """
        Represents an event when a rating is added to a charging station.
        """
        if not isinstance(rating, Rating):
            raise TypeError("rating must be an instance of Rating")
        self.rating: Rating = rating

    def __repr__(self) -> str:
        """
        Returns a string representation of the RatingAddedEvent.
        """
        return f"<RatingAddedEvent(station_id={self.rating.station_id}, rating_value={self.rating.value}, timestamp={self.rating.date})>"
