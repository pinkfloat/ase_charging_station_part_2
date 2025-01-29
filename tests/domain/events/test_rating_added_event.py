# tests/domain/events/test_rating_added_event.py
import pytest
from datetime import datetime
from domain.events.rating_added_event import RatingAddedEvent
from domain.entities.rating import Rating

def test_rating_added_event_initialization():
    rating = Rating(user_id="user_123", station_id=1, date="2025-01-01", value=4, comment="Great station!")

    event = RatingAddedEvent(rating=rating)

    assert event.rating == rating
    assert event.rating.station_id == 1
    assert event.rating.value == 4
    assert event.rating.comment == "Great station!"
    assert isinstance(event.rating.date, str)
    # Verify date is valid ISO format
    datetime_obj = datetime.fromisoformat(event.rating.date)
    assert isinstance(datetime_obj, datetime)

def test_rating_added_event_repr():
    rating = Rating(user_id="user_123", station_id=1, date="2025-01-01", value=4, comment="Great station!")

    event = RatingAddedEvent(rating=rating)

    event_repr = repr(event)

    expected_repr = "<RatingAddedEvent(station_id=1, rating_value=4, timestamp=2025-01-01)>"
    assert event_repr == expected_repr

def test_rating_added_event_invalid_rating():
    invalid_rating = {"user_id": "user_123", "station_id": 1, "date": "2025-01-01", "value": 4, "comment": "Great station!"}

    with pytest.raises(TypeError, match="rating must be an instance of Rating"):
        RatingAddedEvent(rating=invalid_rating)
