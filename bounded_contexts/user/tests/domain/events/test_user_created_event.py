# user/tests/domain/events/test_user_created_event.py
import pytest
from datetime import datetime
from user.src.domain.events.user_created_event import UserCreatedEvent
from user.src.domain.entities.user import User

def test_user_created_event_initialization():
    user = User(id="user_123", name="pinkfloat", password="abcdefgh", date_joined="2025-01-01")
    event = UserCreatedEvent(user=user)

    assert event.user == user
    assert event.user.id == "user_123"
    assert event.user.name == "pinkfloat"
    assert event.user.password == "abcdefgh"
    assert event.user.date_joined == "2025-01-01"

    assert isinstance(event.user.date_joined, str)
    # Verify date is valid ISO format
    datetime_obj = datetime.fromisoformat(event.user.date_joined)
    assert isinstance(datetime_obj, datetime)

def test_user_created_event_repr():
    user = User(id="user_123", name="pinkfloat", password="abcdefgh", date_joined="2025-01-01")
    event = UserCreatedEvent(user=user)

    event_repr = repr(event)

    expected_repr = "<UserCreatedEvent(user_id=user_123, user_name=pinkfloat, timestamp=2025-01-01)>"
    assert event_repr == expected_repr

def test_user_created_event_invalid_user():
    invalid_user = {"id": "user_123", "name": "pinkfloat", "date": "2025-01-01"}

    with pytest.raises(TypeError, match="user must be an instance of User"):
        UserCreatedEvent(user=invalid_user)
