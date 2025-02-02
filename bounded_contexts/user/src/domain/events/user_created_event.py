from bounded_contexts.user.src.domain.entities.user import User

class UserCreatedEvent:
    def __init__(self, user: User):
        """
        Represents an event when a user is created.
        """
        if not isinstance(user, User):
            raise TypeError("user must be an instance of User")
        self.user: User = user

    def __repr__(self) -> str:
        """
        Returns a string representation of the UserCreatedEvent.
        """
        return f"<UserCreatedEvent(user_id={self.user.id}, user_name={self.user.name}, timestamp={self.user.date_joined})>"
