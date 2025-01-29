# tests/infrastructure/repositories/test_charging_station_repository.py
import pytest
from io import StringIO
from infrastructure.repositories.charging_station_repository import ChargingStationRepository
from domain.entities.charging_station import ChargingStation
from domain.entities.rating import Rating
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status
from domain.value_objects.rush_hours import RushHours

def test_load_stations_from_csv_valid():
    repo = ChargingStationRepository()

    csv_data = """stationID,stationName,stationOperator,KW,Latitude,Longitude,PLZ
1,Station A,Operator X,50.0,52.60806,13.3044,13467
2,Station B,Operator Y,100.0,52.6117,13.30914,13467
3,Station C,Operator Z,75.0,52.61259,13.30969,13467
"""
    mock_csv_data = StringIO(csv_data)
    stations = repo.load_stations_from_csv(mock_csv_data)

    # Assert that the returned list is not empty
    assert len(stations) == 3

    # Assert that all elements in the list are instances of ChargingStation
    assert all(isinstance(station, ChargingStation) for station in stations)

    for station in stations:
        # Check that the `location` attribute is an instance of Location
        assert isinstance(station.location, Location)
        
        # Check that the `postal_code` attribute is an instance of PostalCode
        assert isinstance(station.postal_code, PostalCode)
        
        # Check that the `status` attribute is an instance of Status
        assert isinstance(station.status, Status)

    # Assert specific properties of the first station
    station = stations[0]
    assert station.station_id == 1
    assert station.name == "Station A"
    assert station.operator == "Operator X"
    assert station.power == 50.0
    assert station.location.latitude == 52.60806
    assert station.location.longitude == 13.3044
    assert station.postal_code.plz == "13467"

def test_load_stations_from_csv_missing_columns():
    repo = ChargingStationRepository()

    csv_data = """stationID,stationName,KW,Latitude,Longitude
1,Station A,50.0,52.60806,13.3044
2,Station B,100.0,52.6117,13.30914
"""
    mock_csv_data = StringIO(csv_data)

    with pytest.raises(ValueError, match="Missing required columns: stationOperator, PLZ"):
        repo.load_stations_from_csv(mock_csv_data)
