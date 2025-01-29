# src/infrastructure/repositories/rated_charging_station_repository.py
from infrastructure.repositories.charging_station_repository import ChargingStationRepository
from infrastructure.repositories.rating_repository import RatingRepository
from domain.entities.rating import Rating

class RatedChargingStationRepository(ChargingStationRepository, RatingRepository):
    def __init__(self, firebase_secret_json):
        ChargingStationRepository.__init__(self)
        RatingRepository.__init__(self, firebase_secret_json)

    def add_rating_to_station(self, rating):
        """Adds a single rating to the ChargingStation with a matching station_id."""
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")

        for station in self.stations:
            if station.station_id == rating.station_id:
                station.ratings.append(rating)
                break

    def add_all_ratings_to_stations(self):
        """Loops through all ratings and assigns them to their corresponding ChargingStations."""
        for rating in self.station_ratings:
            self.add_rating_to_station(rating)
