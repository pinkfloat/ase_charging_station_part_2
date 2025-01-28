# src/infrastructure/repositories/charging_station_repository.py
import pandas as pd
from domain.aggregates.charging_station import ChargingStation
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status
from domain.value_objects.rush_hours import RushHours

class ChargingStationRepository:
    REQUIRED_COLUMNS = ['stationID', 'stationName', 'stationOperator', 'KW', 'Latitude', 'Longitude', 'PLZ']

    def __init__(self):
        self.stations = []

    def load_from_csv(self, csv_file):
        df = pd.read_csv(csv_file)

        # Validate that all required columns are present
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        # Process the rows to create ChargingStation objects
        for _, row in df.iterrows():
            location = Location(latitude=row['Latitude'], longitude=row['Longitude'])
            postal_code = PostalCode(row['PLZ'])
            time_slots = ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM"]

            station = ChargingStation(
                station_id=row['stationID'],
                name=row['stationName'],
                operator=row['stationOperator'],
                power=row['KW'],
                location=location,
                postal_code=postal_code,
                status=Status.get_random_status(),
                rush_hour_data=RushHours.generate_random_data(time_slots)
            )
            self.stations.append(station)

        return self.stations
