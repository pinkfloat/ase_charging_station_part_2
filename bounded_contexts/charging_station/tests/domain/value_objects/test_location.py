# charging_station/tests/domain/value_objects/test_location.py
import pytest
from charging_station.src.domain.value_objects.location import Location

# Test valid location initialization (within Berlin's bounds)
def test_location_valid():
    location = Location(latitude=52.5200, longitude=13.4050)  # Central Berlin
    assert location.latitude == 52.5200
    assert location.longitude == 13.4050

# Test non-numeric latitude
def test_location_invalid_latitude_non_numeric():
    with pytest.raises(TypeError):
        Location(latitude="not_a_number", longitude=13.4050)  # Non-numeric latitude

# Test non-numeric longitude
def test_location_invalid_longitude_non_numeric():
    with pytest.raises(TypeError):
        Location(latitude=52.5200, longitude="not_a_number")  # Non-numeric longitude

# Test edge case latitude and longitude values around Berlin
def test_location_edge_case():
    location = Location(latitude=52.6755, longitude=13.7612)  # Upper boundary values for Berlin
    assert location.latitude == 52.6755
    assert location.longitude == 13.7612 
