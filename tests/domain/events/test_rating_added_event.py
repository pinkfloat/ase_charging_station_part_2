# tests/domain/events/rating_added_event.py
import pytest
from datetime import datetime
from domain.events.rating_added_event import RatingAddedEvent
from domain.value_objects.rating import Rating

def test_rating_added_event_initialization():
    station_id = 1
    rating = Rating(user_name="user123", value=4, comment="Great station!")

    event = RatingAddedEvent(station_id=station_id, rating=rating)

    assert event.station_id == station_id
    assert event.rating == rating
    assert isinstance(event.timestamp, str)  # Ensure timestamp is an ISO-formatted string
    # Parse timestamp to verify it's a valid datetime
    datetime_obj = datetime.fromisoformat(event.timestamp)
    assert isinstance(datetime_obj, datetime)

def test_rating_added_event_repr():
    station_id = 1
    rating = Rating(user_name="user123", value=4, comment="Great station!")
    timestamp = "2025-01-01T12:00:00"
    event = RatingAddedEvent(station_id=station_id, rating=rating, timestamp=timestamp)

    event_repr = repr(event)

    expected_repr = f"<RatingAddedEvent(station_id={station_id}, rating_value={rating.value}, timestamp={timestamp})>"
    assert event_repr == expected_repr

def test_rating_added_event_invalid_rating():
    station_id = 1
    invalid_rating = {"user_name": "user123", "value": 4, "comment": "Great station!"}

    with pytest.raises(TypeError, match="rating must be an instance of Rating"):
        RatingAddedEvent(station_id=station_id, rating=invalid_rating)

def test_rating_added_event_custom_timestamp():
    station_id = 1
    rating = Rating(user_name="user123", value=5, comment="Excellent station!")
    custom_timestamp = "2025-01-01T15:30:00"

    event = RatingAddedEvent(station_id=station_id, rating=rating, timestamp=custom_timestamp)

    assert event.timestamp == custom_timestamp
