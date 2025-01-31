# charging_station/tests/domain/aggregates/test_rated_charging_station.py
import pytest
from unittest.mock import Mock
from bounded_contexts.charging_station.src.domain.aggregates.rated_charging_station import RatedChargingStation
from bounded_contexts.charging_station.src.domain.events.rating_added_event import RatingAddedEvent
from bounded_contexts.charging_station.src.domain.entities.rating import Rating
from bounded_contexts.charging_station.src.domain.value_objects.location import Location
from bounded_contexts.charging_station.src.domain.value_objects.postal_code import PostalCode
from bounded_contexts.charging_station.src.domain.value_objects.status import Status
from bounded_contexts.charging_station.src.domain.value_objects.rush_hours import RushHours

# Helper function to create valid dependencies
def valid_location():
    return Location(latitude=52.5200, longitude=13.4050)  # Berlin center

def valid_postal_code():
    return PostalCode("10115")

def valid_status():
    return Status.AVAILABLE

def valid_rating():
    return Rating(user_id="user_123", station_id=1, date="2023-01-01", value=5, comment="Great station!")

def valid_rush_hour_data():
    return RushHours(["6 AM", "7 AM", "8 AM", "9 AM"], [2.5, 3.0, 4.5, 1.0])

# Test valid initialization
def test_charging_station_valid_initialization():

    station = RatedChargingStation(
        station_id=1,
        name="Supercharger",
        operator="Tesla",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    assert station.station_id == 1
    assert station.name == "Supercharger"
    assert station.operator == "Tesla"
    assert station.power == 150
    assert isinstance(station.location, Location)
    assert isinstance(station.postal_code, PostalCode)
    assert isinstance(station.status, Status)
    assert station.ratings == []

# Test invalid station_id type
def test_charging_station_invalid_station_id_type():
    with pytest.raises(TypeError, match="station_id must be an int"):
        RatedChargingStation(
            station_id="invalid",  # Invalid station_id type
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code=valid_postal_code(),
            status=valid_status(),
            rush_hour_data=valid_rush_hour_data(),
        )

# Test invalid power type
def test_charging_station_invalid_power_type():
    with pytest.raises(TypeError, match="power must be a float or an int"):
        RatedChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power="invalid",  # Invalid power type
            location=valid_location(),
            postal_code=valid_postal_code(),
            status=valid_status(),
            rush_hour_data=valid_rush_hour_data(),
        )

# Test invalid location type
def test_charging_station_invalid_location_type():
    with pytest.raises(TypeError, match="location must be an instance of Location"):
        RatedChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location="invalid", # Invalid location
            postal_code=valid_postal_code(),
            status=valid_status(),
            rush_hour_data=valid_rush_hour_data(),
        )

# Test invalid postal_code type
def test_charging_station_invalid_postal_code_type():
    with pytest.raises(TypeError, match="postal_code must be an instance of PostalCode"):
        RatedChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code="12345", # Invalid postal code
            status=valid_status(),
            rush_hour_data=valid_rush_hour_data(),
        )

# Test invalid status type
def test_charging_station_invalid_status_type():
    with pytest.raises(TypeError, match="status must be an instance of Status"):
        RatedChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code=valid_postal_code(),
            status="INVALID_STATUS", # Invalid status
            rush_hour_data=valid_rush_hour_data(),
        )

# Test invalid rush_hour_data type
def test_charging_station_invalid_rush_hour_data_type():
    with pytest.raises(TypeError, match="rush_hour_data must be an instance of RushHours"):
        RatedChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code=valid_postal_code(),
            status=valid_status(),
            rush_hour_data="INVALID_DATA", # Invalid rush hour data
        )

# Test adding a valid rating
def test_add_valid_rating():
    station = RatedChargingStation(
        station_id=1,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    rating = valid_rating()
    station.add_rating(rating)

    # Assert the rating was added successfully
    assert len(station.ratings) == 1
    assert station.ratings[0] == rating

# Test adding an invalid rating
def test_add_invalid_rating():
    station = RatedChargingStation(
        station_id=2,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    with pytest.raises(ValueError, match="Invalid rating object"):
        station.add_rating("not_a_rating")  # Invalid input


# Test the average_rating method

# Test when there are no ratings
def test_average_rating_no_ratings():
    station = RatedChargingStation(
        station_id=3,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    # Assert that the average is 0.0 when there are no ratings
    assert station.average_rating() == 0.0

# Test when there is one rating
def test_average_rating_one_rating():
    station = RatedChargingStation(
        station_id=4,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    station.add_rating(Rating(user_id="user_123", station_id=1, date="2023-01-01", value=5, comment="Great!"))

    # Assert that the average equals the single rating value
    assert station.average_rating() == 5.0

# Test when there are multiple ratings
def test_average_rating_multiple_ratings():
    station = RatedChargingStation(
        station_id=5,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
    )

    # Add multiple ratings
    station.add_rating(Rating(user_id="user_1", station_id=1, date="2023-01-01", value=4, comment="Good"))
    station.add_rating(Rating(user_id="user_2", station_id=1, date="2023-01-01", value=3, comment="Okay"))
    station.add_rating(Rating(user_id="user_3", station_id=1, date="2023-01-01", value=5, comment="Excellent"))

    # Assert the average is calculated correctly
    assert station.average_rating() == pytest.approx((4 + 3 + 5) / 3, 0.001)

def test_publish_event():
    mock_event_publisher = Mock()
    station = RatedChargingStation(
        station_id=6,
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
        rush_hour_data=valid_rush_hour_data(),
        event_publisher=mock_event_publisher,
    )

    rating = Rating(user_id="user_15", station_id=8, date="2023-01-01", value=5, comment="Great station!")
    test_event = RatingAddedEvent(rating)
    station.publish_event(test_event)

    mock_event_publisher.assert_called_once_with(test_event)
