# charging_station/src/domain/value_objects/status.py
import random
from enum import Enum

class Status(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    OUT_OF_SERVICE = "out of service"
    MAINTENANCE = "maintenance"

    def __str__(self):
        return self.value

    @staticmethod
    def get_random_status():
        """Returns a random Status value."""
        return random.choice(list(Status))
