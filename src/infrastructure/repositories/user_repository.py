# src/infrastructure/repositories/user_repository.py
from firebase_admin import credentials, initialize_app, db
from domain.aggregates.user import User

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

    def check_if_username_exists(self, name):
        return

    def create_user(self, name, password):
        return
