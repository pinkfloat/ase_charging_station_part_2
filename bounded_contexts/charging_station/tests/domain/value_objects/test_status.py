# charging_station/tests/domain/value_objects/test_status.py
import pytest
from charging_station.src.domain.value_objects.status import Status

# Test that all expected statuses are defined
def test_status_enum_values():
    assert Status.AVAILABLE.value == "available"
    assert Status.OCCUPIED.value == "occupied"
    assert Status.OUT_OF_SERVICE.value == "out of service"
    assert Status.MAINTENANCE.value == "maintenance"

# Test the __str__ method
def test_status_str_method():
    assert str(Status.AVAILABLE) == "available"
    assert str(Status.OCCUPIED) == "occupied"
    assert str(Status.OUT_OF_SERVICE) == "out of service"
    assert str(Status.MAINTENANCE) == "maintenance"

# Test that accessing a status via its name works as expected
def test_status_by_name():
    assert Status["AVAILABLE"] == Status.AVAILABLE
    assert Status["OCCUPIED"] == Status.OCCUPIED

# Test that accessing a status by value works as expected
def test_status_by_value():
    assert Status("available") == Status.AVAILABLE
    assert Status("occupied") == Status.OCCUPIED
    assert Status("out of service") == Status.OUT_OF_SERVICE
    assert Status("maintenance") == Status.MAINTENANCE

# Test invalid value raises ValueError
def test_invalid_status_value():
    with pytest.raises(ValueError, match="is not a valid Status"):
        Status("invalid_value")

# Test the get_random_status function
def test_get_random_status():
    for _ in range(100):  # Run multiple iterations to ensure randomness is covered
        random_status = Status.get_random_status()
        assert random_status in Status
