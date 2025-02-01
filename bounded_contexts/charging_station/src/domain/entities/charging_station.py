# charging_station/src/domain/entities/charging_station.py
class ChargingStation:
    def __init__(self, station_id: int, name: str, operator: str, power: float) -> None:
        """
        Initializes a ChargingStation entity.
        """
        if not isinstance(power, (int, float)):
            raise TypeError("power must be a float or an int")
        if not isinstance(station_id, int):
            raise TypeError("station_id must be an int")

        self.station_id: int = station_id
        self.name: str = name
        self.operator: str = operator
        self.power: float = power
