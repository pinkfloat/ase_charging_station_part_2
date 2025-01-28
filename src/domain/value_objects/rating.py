# src/domain/value_objects/rating.py
class Rating:
    def __init__(self, user_name, value, comment=""):
        if not isinstance(value, int):
            raise ValueError("Rating must be an integer")
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(comment, str):
            raise ValueError("Comment must be a string")
        
        self.user_name = user_name
        self.value = value
        self.comment = comment
