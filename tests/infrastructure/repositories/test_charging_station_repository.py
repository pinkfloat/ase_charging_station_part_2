# tests/infrastructure/repositories/test_charging_station_repository.py
import pytest
from io import StringIO
from infrastructure.repositories.charging_station_repository import ChargingStationRepository
from domain.aggregates.charging_station import ChargingStation
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status
from domain.value_objects.rating import Rating

#_____________________________________Test Database Functions____________________________________

@pytest.fixture
def mock_database(monkeypatch):
    """Mock the Firebase database using monkeypatch."""
    # Mock data to simulate Firebase DB
    mock_data = {
        "rating1": {
            "user_id": "user_123",
            "charging_station_id": 1,
            "review_date": "2025-01-01",
            "review_star": 4,
            "review_text": "Great station!"
        },
        "rating2": {
            "user_id": "user_456",
            "charging_station_id": 2,
            "review_date": "2025-01-02",
            "review_star": 5,
            "review_text": "Excellent service!"
        },
    }

    class MockFirebaseDB:
        def __init__(self):
            self.data = mock_data
            self._apps = ["something"]  # Simulate the _apps attribute

        def reference(self, path):
            return self

        def get(self):
            return self.data

        def child(self, rating_id):
            self.rating_id = rating_id
            return self

        def set(self, rating_data):
            self.data[self.rating_id] = rating_data

    mock_db = MockFirebaseDB()

    # Patch the ChargingStationRepository's db attribute
    monkeypatch.setattr("infrastructure.repositories.charging_station_repository.db", mock_db)
    return mock_db

def test_load_station_ratings_from_database(mock_database):
    repo = ChargingStationRepository("mocked_path")
    ratings = repo.load_station_ratings_from_database()

    assert len(ratings) == 2
    assert ratings[0].user_id == "user_123"
    assert ratings[0].station_id == 1
    assert ratings[0].date == "2025-01-01"
    assert ratings[0].value == 4
    assert ratings[0].comment == "Great station!"

    assert ratings[1].user_id == "user_456"
    assert ratings[1].station_id == 2
    assert ratings[1].date == "2025-01-02"
    assert ratings[1].value == 5
    assert ratings[1].comment == "Excellent service!"

def test_load_station_ratings_from_empty_database(monkeypatch):
    class EmptyFirebaseDB:
        def __init__(self):
            self._apps = ["something"]  # Simulate the _apps attribute

        def reference(self, path):
            return self

        def get(self):
            return {}

    monkeypatch.setattr("infrastructure.repositories.charging_station_repository.db", EmptyFirebaseDB())
    repo = ChargingStationRepository("mocked_path")
    ratings = repo.load_station_ratings_from_database()

    assert len(ratings) == 0

def test_create_rating(mock_database):
    repo = ChargingStationRepository("mocked_path")

    user_id = "user_123"
    station_id = 3
    value= 3
    comment= "Meh"

    station = repo.create_rating(user_id, station_id, value, comment)

    assert isinstance(station, Rating)
    assert station.user_id == user_id
    assert station.station_id == station_id
    assert station.value == value
    assert station.comment == comment

#________________________________________Test CSV reading________________________________________

def test_load_stations_from_csv_valid(mock_database):
    repo = ChargingStationRepository("mocked_path")

    csv_data = """stationID,stationName,stationOperator,KW,Latitude,Longitude,PLZ
1,Station A,Operator X,50.0,52.60806,13.3044,13467
2,Station B,Operator Y,100.0,52.6117,13.30914,13467
3,Station C,Operator Z,75.0,52.61259,13.30969,13467
"""
    mock_csv_data = StringIO(csv_data)
    stations = repo.load_stations_from_csv(mock_csv_data)

    # Assert that the returned list is not empty
    assert len(stations) == 3

    # Assert that all elements in the list are instances of ChargingStation
    assert all(isinstance(station, ChargingStation) for station in stations)

    for station in stations:
        # Check that the `location` attribute is an instance of Location
        assert isinstance(station.location, Location)
        
        # Check that the `postal_code` attribute is an instance of PostalCode
        assert isinstance(station.postal_code, PostalCode)
        
        # Check that the `status` attribute is an instance of Status
        assert isinstance(station.status, Status)

    # Assert specific properties of the first station
    station = stations[0]
    assert station.station_id == 1
    assert station.name == "Station A"
    assert station.operator == "Operator X"
    assert station.power == 50.0
    assert station.location.latitude == 52.60806
    assert station.location.longitude == 13.3044
    assert station.postal_code.plz == "13467"

def test_load_stations_from_csv_missing_columns(mock_database):
    repo = ChargingStationRepository("mocked_path")

    csv_data = """stationID,stationName,KW,Latitude,Longitude
1,Station A,50.0,52.60806,13.3044
2,Station B,100.0,52.6117,13.30914
"""
    mock_csv_data = StringIO(csv_data)

    with pytest.raises(ValueError, match="Missing required columns: stationOperator, PLZ"):
        repo.load_stations_from_csv(mock_csv_data)
