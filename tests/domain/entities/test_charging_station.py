# tests/domain/entities/test_charging_station.py
import pytest
from domain.entities.charging_station import ChargingStation

# Test valid initialization
def test_charging_station_valid_initialization():

    station = ChargingStation(
        station_id=1,
        name="Supercharger",
        operator="Tesla",
        power=150,
    )

    assert station.station_id == 1
    assert station.name == "Supercharger"
    assert station.operator == "Tesla"
    assert station.power == 150

# Test invalid station_id type
def test_charging_station_invalid_station_id_type():
    with pytest.raises(TypeError, match="station_id must be an int"):
        ChargingStation(
            station_id="invalid",  # Invalid station_id type
            name="Supercharger",
            operator="Tesla",
            power=150,
        )

# Test invalid power type
def test_charging_station_invalid_power_type():
    with pytest.raises(TypeError, match="power must be a float or an int"):
        ChargingStation(
            station_id=1,
            name="Supercharger",
            operator="Tesla",
            power="invalid",  # Invalid power type
        )
