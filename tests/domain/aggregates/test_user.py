# tests/domain/aggregates/test_user.py
import pytest
from datetime import datetime
from domain.aggregates.user import User

class TestUser:
    def test_user_creation_valid(self):
        user_id = "user_1"
        name = "Valid_Name_123"
        password = "abcdefgh"
        date_joined = datetime.now().isoformat()
        
        user = User(id=user_id, name=name, password=password, date_joined=date_joined)
        
        assert user.id == user_id
        assert user.name == name
        assert user.password == "abcdefgh"
        assert user.date_joined == date_joined
    
    def test_invalid_user_id(self):
        # Invalid ID format
        with pytest.raises(ValueError, match="Invalid user ID format"):
            User(id="invalid_id", name="ValidName", password="ValidP@ssw0rd", date_joined=datetime.now().isoformat())
    
    def test_invalid_name(self):
        # Name is empty
        with pytest.raises(ValueError, match="Name cannot be empty"):
            User(id="user_1", name="", password="ValidP@ssw0rd", date_joined=datetime.now().isoformat())
    
    def test_invalid_password(self):
        # Password is empty
        with pytest.raises(ValueError, match="Password cannot be empty"):
            User(id="user_1", name="ValidName", password="", date_joined=datetime.now().isoformat())

    def test_invalid_date_joined(self):
        # Invalid date format
        with pytest.raises(ValueError, match="Date must be in ISO 8601 format"):
            User(id="user_1", name="ValidName", password="ValidP@ssw0rd", date_joined="InvalidDate")
