# charging_station/src/domain/value_objects/rush_hours.py
import numpy as np
from typing import List

class RushHours:
    def __init__(self, time_slots: List[str], data: np.ndarray) -> None:
        """
        Initializes a RushHours value object.
        """
        if len(time_slots) != len(data):
            raise ValueError("Length of data must match length of time_slots")
        self.time_slots: List[str] = time_slots
        self.data: np.ndarray = data

    @staticmethod
    def generate_random_data(time_slots: List[str], mean: float = 2.5, std_dev: float = 1.0, min_val: float = 0, max_val: float = 5) -> 'RushHours':
        """
        Generates random rush hour data based on a normal distribution and returns a RushHours object.
        """
        data = np.random.normal(loc=mean, scale=std_dev, size=len(time_slots))
        data = np.clip(data, min_val, max_val)  # Clip data to the specified range
        return RushHours(time_slots, data)

    def to_dict(self) -> dict:
        """
        Converts the RushHours object to a dictionary where time slots are keys and data values are values.
        """
        return dict(zip(self.time_slots, self.data))

    @staticmethod
    def from_dict(data_dict: dict) -> 'RushHours':
        """
        Creates a RushHours object from a dictionary of time slots and corresponding data.
        """
        time_slots = list(data_dict.keys())
        data = list(data_dict.values())
        return RushHours(time_slots, np.array(data))
