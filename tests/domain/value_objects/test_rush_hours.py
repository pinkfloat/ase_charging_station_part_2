# tests/domain/value_objects/test_rush_hours.py
import pytest
import numpy as np
from domain.value_objects.rush_hours import RushHours

def test_rush_hours_initialization():
    time_slots = ["6 AM", "7 AM", "8 AM", "9 AM"]
    data = np.array([2.5, 3.0, 4.5, 1.0])
    rush_hours = RushHours(time_slots, data)

    assert rush_hours.time_slots == time_slots
    assert np.array_equal(rush_hours.data, data)

def test_rush_hours_data_validation():
    time_slots = ["6 AM", "7 AM"]
    data = np.array([2.5])  # Mismatched length
    with pytest.raises(ValueError, match="Length of data must match length of time_slots"):
        RushHours(time_slots, data)

def test_rush_hours_generate_random_data():
    time_slots = ["6 AM", "7 AM", "8 AM", "9 AM"]
    rush_hours = RushHours.generate_random_data(time_slots, mean=2.5, std_dev=1.0, min_val=0, max_val=5)

    assert rush_hours.time_slots == time_slots
    assert len(rush_hours.data) == len(time_slots)
    assert np.all(rush_hours.data >= 0)
    assert np.all(rush_hours.data <= 5)

def test_rush_hours_to_dict():
    time_slots = ["6 AM", "7 AM"]
    data = np.array([2.5, 3.0])
    rush_hours = RushHours(time_slots, data)
    result = rush_hours.to_dict()

    assert result == {"6 AM": 2.5, "7 AM": 3.0}

def test_rush_hours_from_dict():
    data_dict = {"6 AM": 2.5, "7 AM": 3.0}
    rush_hours = RushHours.from_dict(data_dict)

    assert rush_hours.time_slots == ["6 AM", "7 AM"]
    assert np.array_equal(rush_hours.data, np.array([2.5, 3.0]))
