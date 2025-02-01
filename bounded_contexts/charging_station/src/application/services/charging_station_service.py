# charging_station/src/application/services/charging_station_service.py
from charging_station.src.infrastructure.repositories.rated_charging_station_repository import RatedChargingStationRepository

class ChargingStationService:
    def __init__(self, repository: RatedChargingStationRepository, event_publisher=None):
        """
        Initializes a ChargingStationService instance.
        """
        if not isinstance(repository, RatedChargingStationRepository):
            raise TypeError("repository must be an instance of RatedChargingStationRepository")
        self.repository = repository
        self.event_publisher = event_publisher or (lambda event: None)

    def load_stations_from_csv(self, csv_file):
        """
        Loads charging stations from a CSV file via the repository.
        """
        return self.repository.load_stations_from_csv(csv_file, self.event_publisher)
    
    def load_all_ratings_to_stations(self):
        """
        Loads all ratings from the database and assigns them to the corresponding charging stations.
        """
        self.repository.load_station_ratings_from_database()
        self.repository.add_all_ratings_to_stations()
    
    def add_rating_to_station(self, user_id: str, station_id: int, value: int, comment: str):
        """
        Creates a new rating, saves it to the repository, assigns it to the station, and stores it in the database.
        
        Note: This is insecure as writing to database might fail (due to external errors like a lost internet
        connection), thus a more correct function would stop if the writing to the database fails.
        """
        rating = self.repository.create_rating(user_id, station_id, value, comment)
        self.repository.save_rating_to_database(rating)
        self.repository.save_rating_to_repo(rating)
        self.repository.add_rating_to_station(rating)
