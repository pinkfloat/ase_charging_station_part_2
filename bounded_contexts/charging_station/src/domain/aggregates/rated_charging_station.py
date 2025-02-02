# charging_station/src/domain/aggregates/rated_charging_station.py
from typing import Optional, Callable
from bounded_contexts.charging_station.src.domain.events.rating_added_event import RatingAddedEvent
from bounded_contexts.charging_station.src.domain.entities.charging_station import ChargingStation
from bounded_contexts.charging_station.src.domain.entities.rating import Rating
from bounded_contexts.charging_station.src.domain.value_objects.location import Location
from bounded_contexts.charging_station.src.domain.value_objects.postal_code import PostalCode
from bounded_contexts.charging_station.src.domain.value_objects.status import Status
from bounded_contexts.charging_station.src.domain.value_objects.rush_hours import RushHours

class RatedChargingStation(ChargingStation):
    def __init__(
        self,
        station_id: int,
        name: str,
        operator: str,
        power: float,
        location: Location,
        postal_code: PostalCode,
        status: Status,
        rush_hour_data: RushHours,
        event_publisher: Optional[Callable[[object], None]] = None
    ) -> None:
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
        self.ratings: list[Rating] = []  # Explicit type hint for ratings list

        # Dependency Injection for Event-Publisher
        self.event_publisher = event_publisher or (lambda event: None)

    def publish_event(self, event: object) -> None:
        """
        Publishes an event using the injected event publisher.
        """
        self.event_publisher(event)

    def add_rating(self, rating: Rating) -> None:
        """
        Adds a rating to the station and publishes a RatingAddedEvent.
        """
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.ratings.append(rating)

        # Create a RatingAddedEvent and publish it
        event = RatingAddedEvent(rating)
        self.publish_event(event)

    def average_rating(self) -> float:
        """
        Calculates the average rating for the charging station.
        """
        if not self.ratings:
            return 0.0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)
