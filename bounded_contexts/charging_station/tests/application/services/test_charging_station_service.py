# charging_station/tests/application/services/test_charging_station_service.py
import pytest
from unittest.mock import MagicMock
from charging_station.src.application.services.charging_station_service import ChargingStationService
from charging_station.src.infrastructure.repositories.rated_charging_station_repository import RatedChargingStationRepository

@pytest.fixture
def mock_repository():
    return MagicMock(spec=RatedChargingStationRepository)

@pytest.fixture
def service(mock_repository):
    return ChargingStationService(mock_repository)

def test_init_with_invalid_repository():
    with pytest.raises(TypeError):
        ChargingStationService(repository="invalid")

def test_load_all_ratings_to_stations(service, mock_repository):
    service.load_all_ratings_to_stations()
    mock_repository.load_station_ratings_from_database.assert_called_once()
    mock_repository.add_all_ratings_to_stations.assert_called_once()

def test_add_rating_to_station(service, mock_repository):
    user_id = "user123"
    station_id = 1  # Ensure station_id is an integer
    value = 5
    comment = "Great station!"
    mock_rating = MagicMock()
    
    mock_repository.create_rating.return_value = mock_rating
    
    service.add_rating_to_station(user_id, station_id, value, comment)
    
    mock_repository.create_rating.assert_called_once_with(user_id, station_id, value, comment)
    mock_repository.save_rating_to_repo.assert_called_once_with(mock_rating)
    mock_repository.add_rating_to_station.assert_called_once_with(mock_rating)
    mock_repository.save_rating_to_database.assert_called_once_with(mock_rating) 
