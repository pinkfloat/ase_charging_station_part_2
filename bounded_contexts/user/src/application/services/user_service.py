# user/src/application/services/user_service.py
from bounded_contexts.user.src.infrastructure.repositories.user_repository import UserRepository
from bounded_contexts.user.src.domain.entities.user import User

class UserService:
    def __init__(self, user_repository: UserRepository, event_publisher=None):
        """
        Initializes the UserService with the provided UserRepository and optional event publisher.
        """
        self.user_repository = user_repository
        self.user_repository.event_publisher = event_publisher or (lambda event: None)
    
    def get_all_users(self) -> list:
        """
        Loads and returns all users from the database.
        """
        return self.user_repository.load_from_database()

    def create_user(self, username: str, password: str) -> User:
        """
        Creates a new user and saves it to the database.
        """
        if not username.strip():
            raise ValueError("Username cannot be empty.")
        if not password.strip():
            raise ValueError("Password cannot be empty.")
        
        if self.user_repository.check_if_username_exists(username):
            raise ValueError("Username already exists. Please choose another.")
        
        user_id = self.user_repository.get_next_user_id()

        user = self.user_repository.create_user(user_id, username, password)

        self.user_repository.save_to_repo(user)
        self.user_repository.save_to_database(user)

        return user
