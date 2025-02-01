# user/src/domain/events/user_added_event.py
from user.src.domain.entities.user import User

class UserCreatedEvent:
    def __init__(self, user):
        """
        Represents an event when a user is created.
        """
        if not isinstance(user, User):
            raise TypeError("user must be an instance of User")
        self.user = user

    def __repr__(self):
        """
        Returns a string representation of the UserCreatedEvent.
        """
        return f"<UserCreatedEvent(user_id={self.user.id}, user_name={self.user.name}, timestamp={self.user.date_joined})>"
