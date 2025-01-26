# src/domain/aggregates/charging_station.py
from domain.entities.rating import Rating
from domain.value_objects.location import Location
from domain.value_objects.postal_code import PostalCode

class ChargingStation:
    def __init__(self, station_id, name, operator, power, location, postal_code, status):
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
