# charging_station/tests/domain/entities/test_rating.py
import pytest
from datetime import datetime
from bounded_contexts.charging_station.src.domain.entities.rating import Rating

def test_rating_valid_inputs():
    rating = Rating(user_id="user_123", station_id=1, date="2023-01-01", value=5, comment="Great station!")
    assert rating.user_id == "user_123"
    assert rating.station_id == 1
    assert rating.date == "2023-01-01"
    assert rating.value == 5
    assert rating.comment == "Great station!"

def test_rating_valid_inputs_without_comment():
    rating = Rating(user_id="user_456", station_id=2, date="2023-01-02", value=3)
    assert rating.user_id == "user_456"
    assert rating.station_id == 2
    assert rating.date == "2023-01-02"
    assert rating.value == 3
    assert rating.comment == ""

def test_invalid_user_id_format():
    with pytest.raises(ValueError, match="Invalid user ID format"):
        Rating(user_id="invalid_user", station_id=1, date="2023-01-01", value=5)

def test_invalid_station_id_type():
    with pytest.raises(TypeError, match="station_id must be an int"):
        Rating(user_id="user_123", station_id="station_1", date="2023-01-01", value=5)

def test_invalid_rating_type():
    with pytest.raises(ValueError, match="Rating must be an integer"):
        Rating(user_id="user_123", station_id=1, date="2023-01-01", value="5")

def test_rating_out_of_range_low():
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Rating(user_id="user_123", station_id=1, date="2023-01-01", value=0)

def test_rating_out_of_range_high():
    with pytest.raises(ValueError, match="Rating must be between 1 and 5"):
        Rating(user_id="user_123", station_id=1, date="2023-01-01", value=6)

def test_invalid_comment_type():
    with pytest.raises(ValueError, match="Comment must be a string"):
        Rating(user_id="user_123", station_id=1, date="2023-01-01", value=5, comment=123)

def test_invalid_date_format():
    with pytest.raises(ValueError, match="Date must be in ISO 8601 format"):
        Rating(user_id="user_123", station_id=1, date="01-01-2023", value=5)

def test_invalid_date_non_iso_format():
    with pytest.raises(ValueError, match="Date must be in ISO 8601 format"):
        Rating(user_id="user_123", station_id=1, date="2023/01/01", value=5)

def test_valid_date_with_iso_format():
    rating = Rating(user_id="user_123", station_id=1, date="2023-05-20", value=4)
    assert rating.date == "2023-05-20"
