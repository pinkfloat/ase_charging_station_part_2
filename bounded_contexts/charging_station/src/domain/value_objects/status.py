# charging_station/src/domain/value_objects/status.py
import random
from enum import Enum
from typing import List

class Status(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    OUT_OF_SERVICE = "out of service"
    MAINTENANCE = "maintenance"

    def __str__(self) -> str:
        """
        Returns the string representation of the Status value object.
        """
        return self.value

    @staticmethod
    def get_random_status() -> 'Status':
        """
        Returns a random Status value object.
        """
        return random.choice(list(Status))
