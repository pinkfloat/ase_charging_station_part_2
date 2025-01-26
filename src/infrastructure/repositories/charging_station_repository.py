# src/infrastructure/repositories/charging_station_repository.py
from domain.aggregates.charging_station import ChargingStation

class ChargingStationRepository:
    def __init__(self):
        self.stations = []

    def load_from_csv(self, csv_file):
        return
