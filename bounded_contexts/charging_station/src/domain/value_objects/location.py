# charging_station/src/domain/value_objects/location.py
class Location:
    def __init__(self, latitude, longitude):
        """
        Initializes a Location value object.
        """
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise TypeError("Latitude and longitude must be numeric values")
        self.latitude = latitude
        self.longitude = longitude
