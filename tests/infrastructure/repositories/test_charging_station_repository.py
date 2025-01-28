# tests/infrastructure/repositories/test_charging_station_repository.py
import pytest
from io import StringIO
from infrastructure.repositories.charging_station_repository import ChargingStationRepository
from domain.aggregates.charging_station import ChargingStation
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status
from domain.value_objects.rating import Rating
from domain.value_objects.rush_hours import RushHours


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
        
        def push(self, rating_data):
            new_raintg_id = "rating3"
            self.data[new_raintg_id] = rating_data

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

def test_save_rating_to_repo(mock_database):
    repo = ChargingStationRepository("mocked_path")

    rating = Rating("user_123", 4, "2023-01-01T12:00:00", 2, "Urks")
    repo.save_rating_to_repo(rating)

    assert len(repo.station_ratings) == 1
    assert repo.station_ratings[0] == rating

def test_save_invalid_rating_to_repo(mock_database):
    repo = ChargingStationRepository("mocked_path")

    invalid_rating = "This is not a valid rating"
    
    with pytest.raises(ValueError, match="Invalid rating object"):
        repo.save_rating_to_repo(invalid_rating)

def test_save_rating_to_database(mock_database):
    repo = ChargingStationRepository("mocked_path")

    rating = Rating("user_789", 3, "2025-01-03T10:00:00", 5, "Fantastic station!")
    repo.save_rating_to_database(rating)

    saved_rating = mock_database.data["rating3"]
    assert saved_rating["user_id"] == "user_789"
    assert saved_rating["charging_station_id"] == 3
    assert saved_rating["review_star"] == 5
    assert saved_rating["review_text"] == "Fantastic station!"
    assert saved_rating["review_date"] == "2025-01-03T10:00:00"

def test_save_invalid_rating_to_database(mock_database):
    repo = ChargingStationRepository("mocked_path")

    invalid_rating = {
        "user_id": "user_789",
        "value": 5,
        "date": "2025-01-03T10:00:00",
        "station_id": 3,
        "comment": "Fantastic station!"
    }  # Passing a dictionary instead of a Rating object
    
    with pytest.raises(ValueError, match="Invalid rating object"):
        repo.save_rating_to_database(invalid_rating)


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


#______________________________Test Mapping of Ratings to Stations_______________________________

@pytest.fixture
def mock_repository(mock_database):
    repo = ChargingStationRepository("mocked_path")

    # Add mock stations
    station1 = ChargingStation(
        station_id=1,
        name="Station 1",
        operator="Operator 1",
        power=50,
        location=Location(latitude=52.5200, longitude=13.4050),
        postal_code=PostalCode("12345"),
        status=Status.AVAILABLE,
        rush_hour_data=RushHours(["6 AM", "7 AM", "8 AM", "9 AM"], [2.5, 3.0, 4.5, 1.0])
    )

    station2 = ChargingStation(
        station_id=2,
        name="Station 2",
        operator="Operator 2",
        power=75,
        location=Location(latitude=52.5200, longitude=13.4050),
        postal_code=PostalCode("67890"),
        status=Status.AVAILABLE,
        rush_hour_data=RushHours(["6 AM", "7 AM", "8 AM", "9 AM"], [2.5, 3.0, 4.5, 1.0])
    )

    repo.stations = [station1, station2]

    # Add mock ratings
    rating1 = Rating(
        user_id="user_1",
        station_id=1,
        date="2025-01-01",
        value=5,
        comment="Great station!"
    )

    rating2 = Rating(
        user_id="user_2",
        station_id=1,
        date="2025-01-02",
        value=4,
        comment="Good experience."
    )

    rating3 = Rating(
        user_id="user_3",
        station_id=2,
        date="2025-01-03",
        value=3,
        comment="Average service."
    )

    repo.station_ratings = [rating1, rating2, rating3]

    return repo

def test_add_rating_to_station(mock_repository):
    repo = mock_repository
    
    new_rating = Rating(
        user_id="user_4",
        station_id=1,
        date="2025-01-04",
        value=5,
        comment="Excellent!"
    )

    # Simulate that all "old" ratings have already been appended
    repo.add_all_ratings_to_stations()

    # Test if new rating was added
    repo.add_rating_to_station(new_rating)

    station = next((s for s in repo.stations if s.station_id == 1), None)
    assert station is not None
    assert hasattr(station, 'ratings')
    assert len(station.ratings) == 3  # Two initial ratings + one new rating
    assert station.ratings[-1].user_id == "user_4"
    assert station.ratings[-1].comment == "Excellent!"

def test_add_all_ratings_to_stations(mock_repository):
    repo = mock_repository

    repo.add_all_ratings_to_stations()

    # Verify station 1 ratings
    station1 = next((s for s in repo.stations if s.station_id == 1), None)
    assert station1 is not None
    assert hasattr(station1, 'ratings')
    assert len(station1.ratings) == 2  # Two ratings for station_1
    assert station1.ratings[0].user_id == "user_1"
    assert station1.ratings[1].user_id == "user_2"

    # Verify station 2 ratings
    station2 = next((s for s in repo.stations if s.station_id == 2), None)
    assert station2 is not None
    assert hasattr(station2, 'ratings')
    assert len(station2.ratings) == 1  # One rating for station_2
    assert station2.ratings[0].user_id == "user_3"
