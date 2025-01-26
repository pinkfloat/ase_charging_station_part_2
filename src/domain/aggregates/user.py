# src/domain/aggregates/user.py
class User:
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password
