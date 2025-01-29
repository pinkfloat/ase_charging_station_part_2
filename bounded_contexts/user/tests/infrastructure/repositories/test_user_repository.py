# user/tests/infrastructure/repositories/test_user_repository.py
import pytest
import hashlib
from datetime import datetime
from user.src.infrastructure.repositories.user_repository import UserRepository
from user.src.domain.entities.user import User

@pytest.fixture
def mock_database(monkeypatch):
    """Mock the Firebase database using monkeypatch."""
    # Mock data to simulate Firebase DB
    mock_data = {
        "user_1": {
            "username": "test_user",
            "password": hashlib.sha256("secure_password".encode()).hexdigest(),
            "date_joined": "2023-01-01T12:00:00"
        },
        "user_2": {
            "username": "another_user",
            "password": hashlib.sha256("another_password".encode()).hexdigest(),
            "date_joined": "2024-01-01T12:00:00"
        }
    }

    class MockFirebaseDB:
        def __init__(self):
            self.data = mock_data
            self._apps = ["something"]  # Simulate the _apps attribute

        def reference(self, path):
            return self

        def get(self):
            return self.data

        def child(self, user_id):
            self.user_id = user_id
            return self

        def set(self, user_data):
            self.data[self.user_id] = user_data

    mock_db = MockFirebaseDB()

    # Patch the UserRepository's db attribute
    monkeypatch.setattr("user.src.infrastructure.repositories.user_repository.db", mock_db)
    return mock_db

def test_load_from_database(mock_database):
    repo = UserRepository("mocked_path")
    users = repo.load_from_database()

    assert len(users) == 2
    assert users[0].id == "user_1"
    assert users[0].name == "test_user"
    assert users[0].password == repo.hash_password("secure_password")
    assert users[0].date_joined == "2023-01-01T12:00:00"

    assert users[1].id == "user_2"
    assert users[1].name == "another_user"
    assert users[1].password == repo.hash_password("another_password")
    assert users[1].date_joined == "2024-01-01T12:00:00"

def test_load_from_empty_database(monkeypatch):
    class EmptyFirebaseDB:
        def __init__(self):
            self._apps = ["something"]  # Simulate the _apps attribute

        def reference(self, path):
            return self

        def get(self):
            return {}

    monkeypatch.setattr("user.src.infrastructure.repositories.user_repository.db", EmptyFirebaseDB())
    repo = UserRepository("mocked_path")
    users = repo.load_from_database()

    assert len(users) == 0

def test_check_if_username_exists(mock_database):
    repo = UserRepository("mocked_path")
    repo.load_from_database()

    assert repo.check_if_username_exists("test_user") is True
    assert repo.check_if_username_exists("non_existing_user") is False

def test_get_next_user_id(mock_database):
    repo = UserRepository("mocked_path")
    repo.load_from_database()
    repo.users.append(User(id="user_3", name="user3", password="pass", date_joined="2023-01-01T12:00:00"))
    repo.users.append(User(id="user_10", name="user10", password="pass", date_joined="2023-01-01T12:00:00"))

    next_id = repo.get_next_user_id()
    assert next_id == "user_11"

def test_create_user(mock_database):
    repo = UserRepository("mocked_path")

    user_id = "user_123"
    username = "some_user"
    password = "random_password"
    user = repo.create_user(user_id, username, password)

    assert isinstance(user, User)
    assert user.id == user_id
    assert user.name == username.strip()
    assert user.password == hashlib.sha256(password.strip().encode()).hexdigest()
    assert datetime.fromisoformat(user.date_joined)

def test_save_to_repo(mock_database):
    repo = UserRepository("mocked_path")

    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_repo(user)

    assert len(repo.users) == 1
    assert repo.users[0] == user

def test_save_to_repo_invalid_user(mock_database):
    repo = UserRepository("mocked_path")

    with pytest.raises(ValueError, match="Invalid user object"):
        repo.save_to_repo("not_a_user_object")

def test_save_to_database(mock_database):
    repo = UserRepository("mocked_path")

    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_database(user)

    saved_user = mock_database.data["user_123"]
    assert saved_user["username"] == "some_user"
    assert saved_user["password"] == "random_password"
    assert saved_user["date_joined"] == "2023-01-01T12:00:00"

def test_save_invalid_user_to_database(mock_database):
    repo = UserRepository("mocked_path")

    invalid_user = {"id": "user_123", "name": "some_user"}  # Passing a dictionary instead of a User object
    
    with pytest.raises(ValueError, match="Invalid user object"):
        repo.save_to_database(invalid_user)

def test_hash_password(mock_database):
    repo = UserRepository("mocked_path")

    password = "secure_password"
    hashed = repo.hash_password(password)

    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    assert hashed == expected_hash
