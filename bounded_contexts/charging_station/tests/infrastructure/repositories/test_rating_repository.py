# charging_station/tests/infrastructure/repositories/test_rating_repository.py
import pytest
from bounded_contexts.charging_station.src.domain.entities.rating import Rating
from bounded_contexts.charging_station.src.infrastructure.repositories.rating_repository import RatingRepository

import firebase_admin


from unittest.mock import MagicMock
from firebase_admin import credentials


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

    # Patch the RatingRepository's db attribute
    monkeypatch.setattr("charging_station.src.infrastructure.repositories.rating_repository.db", mock_db)
    return mock_db

def test_load_station_ratings_from_database(mock_database, monkeypatch):

    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")
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

    monkeypatch.setattr("charging_station.src.infrastructure.repositories.rating_repository.db", EmptyFirebaseDB())
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")
    ratings = repo.load_station_ratings_from_database()

    assert len(ratings) == 0

def test_create_rating(mock_database, monkeypatch):
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")

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

def test_save_rating_to_repo(mock_database, monkeypatch):
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")

    rating = Rating("user_123", 4, "2023-01-01T12:00:00", 2, "Urks")
    repo.save_rating_to_repo(rating)

    assert len(repo.station_ratings) == 1
    assert repo.station_ratings[0] == rating

def test_save_invalid_rating_to_repo(mock_database, monkeypatch):
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")

    invalid_rating = "This is not a valid rating"
    
    with pytest.raises(ValueError, match="Invalid rating object"):
        repo.save_rating_to_repo(invalid_rating)

def test_save_rating_to_database(mock_database, monkeypatch):
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")

    rating = Rating("user_789", 3, "2025-01-03T10:00:00", 5, "Fantastic station!")
    repo.save_rating_to_database(rating)

    saved_rating = mock_database.data["rating3"]
    assert saved_rating["user_id"] == "user_789"
    assert saved_rating["charging_station_id"] == 3
    assert saved_rating["review_star"] == 5
    assert saved_rating["review_text"] == "Fantastic station!"
    assert saved_rating["review_date"] == "2025-01-03T10:00:00"

def test_save_invalid_rating_to_database(mock_database, monkeypatch):

    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = RatingRepository("mocked_path")

    invalid_rating = {
        "user_id": "user_789",
        "value": 5,
        "date": "2025-01-03T10:00:00",
        "station_id": 3,
        "comment": "Fantastic station!"
    }  # Passing a dictionary instead of a Rating object
    
    with pytest.raises(ValueError, match="Invalid rating object"):
        repo.save_rating_to_database(invalid_rating)




## new additional test cases

def test_firebase_initialization_when_not_initialized(monkeypatch):
    """
    Test that when no Firebase app is initialized (firebase_admin._apps is empty),
    the repository initializes Firebase using the provided certificate and settings.
    """
    # Simulate that no Firebase app is initialized.
    monkeypatch.setattr(firebase_admin, '_apps', [])

    # Create a fake certificate object and a fake initialize_app function.
    fake_cert = MagicMock(name="FakeCertificate")
    fake_initialize_app = MagicMock(name="initialize_app")

    # Patch credentials.Certificate to return our fake_cert.
    monkeypatch.setattr(credentials, 'Certificate', lambda path: fake_cert)

    # Patch initialize_app in the repository's module namespace.
    # Note: Adjust the import path if necessary.
    monkeypatch.setattr(
        "charging_station.src.infrastructure.repositories.rating_repository.initialize_app",
        fake_initialize_app
    )

    # Patch firebase_admin.get_app to return a dummy app after initialization,
    # so that subsequent calls (e.g. db.reference) don't fail.
    monkeypatch.setattr(firebase_admin, 'get_app', lambda name="[DEFAULT]": MagicMock())

    # Provide a fake firebase_secret_json path.
    firebase_secret_json = "path/to/firebase_secret.json"

    # Instantiating the repository should trigger the Firebase initialization.
    _ = RatingRepository(firebase_secret_json)

    # Verify that our fake_initialize_app was called with the fake_cert and the expected databaseURL.
    fake_initialize_app.assert_called_once_with(
        fake_cert,
        {'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'}
    )
