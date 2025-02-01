# charging_station/src/infrastructure/repositories/charging_station_repository.py
import pandas as pd
from typing import List, Optional
from charging_station.src.domain.aggregates.rated_charging_station import RatedChargingStation
from charging_station.src.domain.value_objects.location import Location
from charging_station.src.domain.value_objects.postal_code import PostalCode
from charging_station.src.domain.value_objects.status import Status
from charging_station.src.domain.value_objects.rush_hours import RushHours

class ChargingStationRepository:
    REQUIRED_COLUMNS: List[str] = ['stationID', 'stationName', 'stationOperator', 'KW', 'Latitude', 'Longitude', 'PLZ']

    def __init__(self) -> None:
        """
        Initializes the ChargingStationRepository.
        """
        self.stations: List[RatedChargingStation] = []

    def load_stations_from_csv(self, csv_file: str, event_publisher: Optional[callable] = None) -> List[RatedChargingStation]:
        """
        Loads charging stations from a CSV file, validates columns, 
        and creates a list of ChargingStation objects.
        """
        df = pd.read_csv(csv_file)
        df['stationName'] = df['stationName'].fillna("Unknown")

        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

        for _, row in df.iterrows():
            location = Location(latitude=row['Latitude'], longitude=row['Longitude'])
            postal_code = PostalCode(row['PLZ'])
            time_slots = ["6 AM", "7 AM", "8 AM", "9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM"]

            station = RatedChargingStation(
                station_id=row['stationID'],
                name=row['stationName'],
                operator=row['stationOperator'],
                power=row['KW'],
                location=location,
                postal_code=postal_code,
                status=Status.get_random_status(),
                rush_hour_data=RushHours.generate_random_data(time_slots),
                event_publisher=event_publisher
            )
            self.stations.append(station)

        return self.stations
