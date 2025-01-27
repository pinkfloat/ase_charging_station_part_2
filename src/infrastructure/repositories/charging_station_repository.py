# src/infrastructure/repositories/charging_station_repository.py
import pandas as pd
import random
from domain.aggregates.charging_station import ChargingStation
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status

class ChargingStationRepository:
    def __init__(self):
        self.stations = []
    
    def get_random_status(self):
        random_status = random.choice(list(Status))
        return random_status

    def load_from_csv(self, csv_file):
        df = pd.read_csv(csv_file, usecols=['stationID', 'stationName', 'stationOperator', 'KW', 'Latitude', 'Longitude', 'PLZ'])

        for _, row in df.iterrows():
            location = Location(latitude=row['Latitude'], longitude=row['Longitude'])
            postal_code = PostalCode(row['PLZ'])

            station = ChargingStation(
                station_id=row['stationID'],
                name=row['stationName'],
                operator=row['stationOperator'],
                power=row['KW'],
                location=location,
                postal_code=postal_code,
                status=self.get_random_status()
            )
            self.stations.append(station)

        return self.stations
