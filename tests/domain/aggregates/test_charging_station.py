# tests/domain/aggregates/test_charging_station.py
import pytest
from domain.aggregates.charging_station import ChargingStation
from domain.entities.rating import Rating
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status

# Helper function to create valid dependencies
def valid_location():
    return Location(latitude=52.5200, longitude=13.4050)  # Berlin center

def valid_postal_code():
    return PostalCode("10115")

def valid_status():
    return Status.AVAILABLE

def valid_rating():
    return Rating(user_name="user123", value=4)

# Test valid initialization
def test_charging_station_valid_initialization():

    station = ChargingStation(
        station_id=1,
        name="Supercharger",
        operator="Tesla",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
    )

    assert station.station_id == 1
    assert station.name == "Supercharger"
    assert station.operator == "Tesla"
    assert station.power == 150
    assert isinstance(station.location, Location)
    assert isinstance(station.postal_code, PostalCode)
    assert isinstance(station.status, Status)
    assert station.ratings == []

# Test invalid location type
def test_charging_station_invalid_location_type():
    with pytest.raises(TypeError, match="location must be an instance of Location"):
        ChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location="invalid", # Invalid location
            postal_code=valid_postal_code(),
            status=valid_status(),
        )

# Test invalid postal_code type
def test_charging_station_invalid_postal_code_type():
    with pytest.raises(TypeError, match="postal_code must be an instance of PostalCode"):
        ChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code="12345", # Invalid postal code
            status=valid_status(),
        )

# Test invalid status type
def test_charging_station_invalid_status_type():
    with pytest.raises(TypeError, match="status must be an instance of Status"):
        ChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power=150,
            location=valid_location(),
            postal_code=valid_postal_code(),
            status="INVALID_STATUS", # Invalid status
        )

# Test adding a valid rating
def test_add_valid_rating():
    station = ChargingStation(
        station_id="CS123",
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
    )

    rating = valid_rating()
    station.add_rating(rating)

    # Assert the rating was added successfully
    assert len(station.ratings) == 1
    assert station.ratings[0] == rating

# Test adding an invalid rating
def test_add_invalid_rating():
    station = ChargingStation(
        station_id="CS123",
        name="Berlin Charging Station",
        operator="Green Energy",
        power=150,
        location=valid_location(),
        postal_code=valid_postal_code(),
        status=valid_status(),
    )

    with pytest.raises(ValueError, match="Invalid rating object"):
        station.add_rating("not_a_rating")  # Invalid input
