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
        if not isinstance(power, (int, float)):
            raise TypeError("power must be a float or an int")
        if not isinstance(station_id, int):
            raise TypeError("station_id must be an int")
        
        self.station_id = station_id
        self.name = name
        self.operator = operator
        self.power = power
        self.location = location
        self.postal_code = postal_code
        self.status = status
        self.ratings = []

    def add_rating(self, rating):
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.ratings.append(rating)

    def average_rating(self):
        if not self.ratings:
            return 0.0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)
