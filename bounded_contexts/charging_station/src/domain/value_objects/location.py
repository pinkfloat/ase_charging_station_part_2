# charging_station/src/domain/value_objects/location.py
class Location:
    def __init__(self, latitude, longitude):
        # Ensure the latitude and longitude are numbers
        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise TypeError("Latitude and longitude must be numeric values")
        
        # Validate that the location is within Berlin's approximate geographic bounds
        if not (52.3380 <= latitude <= 52.6755):
            raise ValueError("Latitude must be between 52.3380 and 52.6755 (around Berlin)")
        
        if not (13.0880 <= longitude <= 13.7612):
            raise ValueError("Longitude must be between 13.0880 and 13.7612 (around Berlin)")
        
        self.latitude = latitude
        self.longitude = longitude
