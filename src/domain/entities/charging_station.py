# src/domain/entities/charging_station.py

class ChargingStation:
    def __init__(self, station_id, name, operator, power):
        if not isinstance(power, (int, float)):
            raise TypeError("power must be a float or an int")
        if not isinstance(station_id, int):
            raise TypeError("station_id must be an int")

        self.station_id = station_id
        self.name = name
        self.operator = operator
        self.power = power
