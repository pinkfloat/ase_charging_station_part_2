# user/src/infrastructure/repositories/user_repository.py
import firebase_admin
from firebase_admin import credentials, initialize_app, db
from datetime import datetime
import hashlib

from user.src.domain.entities.user import User
from user.src.domain.events.user_created_event import UserCreatedEvent

class UserRepository:
    def __init__(self, firebase_secret_json, event_publisher=None):
        # Initialize Firebase only once
        if not firebase_admin._apps:  # Check if Firebase is already initialized
            cred = credentials.Certificate(firebase_secret_json)
            initialize_app(cred, {
                'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        
        self.users_ref = db.reference("users")
        self.users = []

        # Dependency Injection for Event-Publisher
        self.event_publisher = event_publisher or (lambda event: None)

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
    
    def publish_event(self, event):
        """Publishes an event using the injected publisher (i.e. flash)."""
        self.event_publisher(event)

    def create_user(self, user_id, username, password):
        """Generates a new user object."""
        user = User(
            id=user_id,
            name=username.strip(),
            password=self.hash_password(password.strip()),
            date_joined=datetime.now().isoformat()
        )

        # Create a UserCreatedEvent and publish it
        event = UserCreatedEvent(user)
        self.publish_event(event)

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
