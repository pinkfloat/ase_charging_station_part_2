# src/domain/aggregates/charging_station.py
from domain.entities.rating import Rating
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode
from domain.value_objects.status import Status

class ChargingStation:
    def __init__(self, station_id, name, operator, power, location, postal_code, status):
        if not isinstance(location, Location):
            raise TypeError("location must be an instance of Location")
        if not isinstance(postal_code, PostalCode):
            raise TypeError("postal_code must be an instance of PostalCode")
        if not isinstance(status, Status):
            raise TypeError("status must be an instance of Status")
        
        self.station_id = station_id
        self.name = name
        self.operator = operator
        self.power = power
        self.location = location
        self.postal_code = postal_code
        self.status = status
        self.ratings = []

    def add_rating(self, rating):
        return

    def average_rating(self):
        return
