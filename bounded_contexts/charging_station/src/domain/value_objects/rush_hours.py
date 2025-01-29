# charging_station/src/domain/value_objects/rush_hours.py
import numpy as np

class RushHours:
    def __init__(self, time_slots, data):
        if len(time_slots) != len(data):
            raise ValueError("Length of data must match length of time_slots")
        self.time_slots = time_slots
        self.data = np.array(data)

    @staticmethod
    def generate_random_data(time_slots, mean=2.5, std_dev=1.0, min_val=0, max_val=5):
        data = np.random.normal(loc=mean, scale=std_dev, size=len(time_slots))
        data = np.clip(data, min_val, max_val)  # Clip data to the specified range
        return RushHours(time_slots, data)

    def to_dict(self):
        return dict(zip(self.time_slots, self.data))

    @staticmethod
    def from_dict(data_dict):
        time_slots = list(data_dict.keys())
        data = list(data_dict.values())
        return RushHours(time_slots, data)
