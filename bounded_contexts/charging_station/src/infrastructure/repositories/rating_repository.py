# charging_station/src/infrastructure/repositories/rating_repository.py
from typing import List
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, initialize_app, db
from bounded_contexts.charging_station.src.domain.entities.rating import Rating

class RatingRepository:
    def __init__(self, firebase_secret_json: str) -> None:
        """
        Initializes the RatingRepository, sets up Firebase connection using the provided secret JSON file.
        """
        if not firebase_admin._apps:  # Check if Firebase is already initialized
            cred = credentials.Certificate(firebase_secret_json)
            initialize_app(cred, {
                'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'
            })
        
        self.station_ratings_ref = db.reference("ratings")
        self.station_ratings: List[Rating] = []
    
    def load_station_ratings_from_database(self) -> List[Rating]:
        """
        Loads all station ratings from the Firebase database and returns them as Rating objects.
        """
        rating_dict = self.station_ratings_ref.get() or {}  # Get all ratings or an empty dictionary

        for rating_id, data in rating_dict.items():
            rating = Rating(
                user_id=data["user_id"],
                station_id=data["charging_station_id"],
                date=data["review_date"],
                value=data["review_star"],
                comment=data["review_text"],
            )
            self.station_ratings.append(rating)
        return self.station_ratings

    def create_rating(self, user_id: str, station_id: int, value: int, comment: str) -> Rating:
        """
        Generates a new rating object.
        """
        rating = Rating(
            user_id=user_id,
            station_id=station_id,
            date=datetime.now().isoformat(),
            value=value,
            comment=comment
        )
        return rating
    
    def save_rating_to_repo(self, rating: Rating) -> None:
        """
        Appends the rating on the repository rating list.
        """
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.station_ratings.append(rating)

    def save_rating_to_database(self, rating: Rating) -> None:
        """
        Saves a new rating to the database.
        """
        if not isinstance(rating, Rating):
            raise ValueError("Invalid rating object")
        self.station_ratings_ref.push({
            "user_id": rating.user_id,
            "charging_station_id": rating.station_id,
            "review_star": rating.value,
            "review_text": rating.comment,
            "review_date": rating.date
        })
