# src/domain/value_objects/status.py
from enum import Enum

class Status(Enum):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    OUT_OF_SERVICE = "out of service"
    MAINTENANCE = "maintenance"

    def __str__(self):
        return self.value
