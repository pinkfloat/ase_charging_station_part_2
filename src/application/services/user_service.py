# src/application/services/user_service.py
from infrastructure.repositories.user_repository import UserRepository

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_all_users(self):
        """Loads and returns all users from the database."""
        return self.user_repository.load_from_database()

    def create_user(self, username, password):
        """Creates a new user and saves it to the database."""
        if not username.strip():
            raise ValueError("Username cannot be empty.")
        if not password.strip():
            raise ValueError("Password cannot be empty.")
        
        # Ensure username is unique
        if self.user_repository.check_if_username_exists(username):
            raise ValueError("Username already exists. Please choose another.")
        
        # Generate next user ID
        user_id = self.user_repository.get_next_user_id()

        # Create new user
        user = self.user_repository.create_user(user_id, username, password)

        # Save user
        self.user_repository.save_to_repo(user)
        self.user_repository.save_to_database(user)

        return user
