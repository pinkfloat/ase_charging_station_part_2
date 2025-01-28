# src/infrastructure/repositories/user_repository.py
from firebase_admin import credentials, initialize_app, db
from domain.entities.user import User
from datetime import datetime
import hashlib

class UserRepository:
    def __init__(self, firebase_secret_json):
        # Initialize Firebase only once
        if not db._apps:  # Check if Firebase is already initialized
            cred = credentials.Certificate(firebase_secret_json)
            initialize_app(cred, {
                'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        
        self.users_ref = db.reference("users")
        self.users = []

    def load_from_database(self):
        user_dict = self.users_ref.get() or {}  # Get all users or an empty dictionary

        for user_id, data in user_dict.items():
            user = User(
                id=user_id,
                name=data["username"],
                password=data["password"],
                date_joined=data["date_joined"]
            )
            self.users.append(user)
        return self.users

    def check_if_username_exists(self, username):
        """Checks if a username exists in the database."""
        for user in self.users:
            if user.name == username:
                return True
        return False
    
    def get_next_user_id(self):
        """Finds the highest existing user ID and generates the next one."""
        max_id = 0
        for user in self.users:
            # Extract the numeric part of the user ID
            user_id_number = int(user.id.split("_")[1])
            max_id = max(max_id, user_id_number)
        return f"user_{max_id + 1}"

    def create_user(self, user_id, username, password):
        """Generates a new user object."""
        user = User(
            id=user_id,
            name=username.strip(),
            password=self.hash_password(password.strip()),
            date_joined=datetime.now().isoformat()
        )
        return user

    def save_to_repo(self, user):
        """Appends the user on the repository users list."""
        if not isinstance(user, User):
            raise ValueError("Invalid user object")
        self.users.append(user)

    def save_to_database(self, user):
        """Saves a new user to the database."""
        if not isinstance(user, User):
            raise ValueError("Invalid user object")
        self.users_ref.child(user.id).set({
            "username": user.name,
            "password": user.password,
            "date_joined": user.date_joined
        })

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
