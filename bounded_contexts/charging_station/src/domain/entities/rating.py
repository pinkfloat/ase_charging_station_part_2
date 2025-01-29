# charging_station/src/domain/entities/rating.py
import re
from datetime import datetime

class Rating:
    def __init__(self, user_id, station_id, date, value, comment=""):
        if not re.match(r"^user_\d+$", user_id):
            raise ValueError("Invalid user ID format")
        if not isinstance(station_id, int):
            raise TypeError("station_id must be an int")
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        try:
            datetime.fromisoformat(date)
        except ValueError:
            raise ValueError("Date must be in ISO 8601 format")
        
        self.user_id = user_id
        self.station_id = station_id
        self.date = date
        self.value = value
        self.comment = comment
