# tests/domain/value_objects/test_location.py
import pytest
from domain.value_objects.location import Location

# Test valid location initialization (within Berlin's bounds)
def test_location_valid():
    location = Location(latitude=52.5200, longitude=13.4050)  # Central Berlin
    assert location.latitude == 52.5200
    assert location.longitude == 13.4050

# Test invalid latitude (out of Berlin's range)
def test_location_invalid_latitude_too_high():
    with pytest.raises(ValueError, match="Latitude must be between 52.3380 and 52.6755"):
        Location(latitude=52.7000, longitude=13.4050)  # Too high latitude

def test_location_invalid_latitude_too_low():
    with pytest.raises(ValueError, match="Latitude must be between 52.3380 and 52.6755"):
        Location(latitude=52.3000, longitude=13.4050)  # Too low latitude

# Test invalid longitude (out of Berlin's range)
def test_location_invalid_longitude_too_high():
    with pytest.raises(ValueError, match="Longitude must be between 13.0880 and 13.7612"):
        Location(latitude=52.5200, longitude=13.8000)  # Too high longitude

def test_location_invalid_longitude_too_low():
    with pytest.raises(ValueError, match="Longitude must be between 13.0880 and 13.7612"):
        Location(latitude=52.5200, longitude=13.0000)  # Too low longitude

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
