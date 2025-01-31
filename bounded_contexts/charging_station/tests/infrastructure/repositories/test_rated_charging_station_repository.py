# charging_station/tests/infrastructure/repositories/test_charging_station_repository.py
import pytest
from bounded_contexts.charging_station.src.infrastructure.repositories.rated_charging_station_repository import RatedChargingStationRepository
from bounded_contexts.charging_station.src.domain.aggregates.rated_charging_station import RatedChargingStation
from bounded_contexts.charging_station.src.domain.entities.rating import Rating
from bounded_contexts.charging_station.src.domain.value_objects.location import Location
from bounded_contexts.charging_station.src.domain.value_objects.postal_code import PostalCode
from bounded_contexts.charging_station.src.domain.value_objects.status import Status
from bounded_contexts.charging_station.src.domain.value_objects.rush_hours import RushHours

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
    monkeypatch.setattr("charging_station.src.infrastructure.repositories.rating_repository.db", mock_db)
    return mock_db


@pytest.fixture
def mock_repository(mock_database):
    repo = RatedChargingStationRepository("mocked_path")

    # Add mock stations
    station1 = RatedChargingStation(
        station_id=1,
        name="Station 1",
        operator="Operator 1",
        power=50,
        location=Location(latitude=52.5200, longitude=13.4050),
        postal_code=PostalCode("12345"),
        status=Status.AVAILABLE,
        rush_hour_data=RushHours(["6 AM", "7 AM", "8 AM", "9 AM"], [2.5, 3.0, 4.5, 1.0])
    )

    station2 = RatedChargingStation(
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
