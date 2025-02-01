# user/src/domain/entities/user.py
import re
from datetime import datetime

class User:
    def __init__(self, id: str, name: str, password: str, date_joined: str):
        """
        Initializes a User entity with the provided details. Validates the user ID format,
        checks that name and password are not empty, and ensures the date_joined is in ISO 8601 format.
        """
        if not re.match(r"^user_\d+$", id):
            raise ValueError("Invalid user ID format")
        if not name:
            raise ValueError("Name cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        try:
            datetime.fromisoformat(date_joined)
        except ValueError:
            raise ValueError("Date must be in ISO 8601 format")
        
        self.id = id
        self.name = name
        self.password = password
        self.date_joined = date_joined
