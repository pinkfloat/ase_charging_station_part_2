# tests/infrastructure/repositories/test_user_repository.py
import pytest
import hashlib
from datetime import datetime
from unittest.mock import patch, MagicMock
from infrastructure.repositories.user_repository import UserRepository
from domain.aggregates.user import User

@pytest.fixture
def mock_firebase_admin():
    # Patch the Firebase initialization
    with patch("infrastructure.repositories.user_repository.db") as mock_db:
    
        password1 = "secure_password"
        password2 = "another_password"
        hashed_password1 = hashlib.sha256(password1.encode()).hexdigest()
        hashed_password2 = hashlib.sha256(password2.encode()).hexdigest()
        
        # Mock Firebase methods
        mock_ref = MagicMock()
        mock_ref.get.return_value = {
            "user_1": {
                "username": "test_user",
                "password": hashed_password1,
                "date_joined": "2023-01-01T12:00:00"
            },
            "user_2": {
                "username": "another_user",
                "password": hashed_password2,
                "date_joined": "2024-01-01T12:00:00"
            }
        }
        mock_db.reference.return_value = mock_ref
        yield mock_db, mock_ref

def test_user_repository_initialization(mock_firebase_admin):
    mock_db, _ = mock_firebase_admin
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    mock_db.reference.assert_called_with("users")

def test_load_from_database(mock_firebase_admin):
    _, mock_ref = mock_firebase_admin
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    users = repo.load_from_database()
    
    # Verify the repository loaded the correct number of users
    assert len(users) == 2
    
    # Check the user attributes
    assert users[0].id == "user_1"
    assert users[0].name == "test_user"
    assert users[0].password == repo.hash_password("secure_password")
    assert users[0].date_joined == "2023-01-01T12:00:00"

    assert users[1].id == "user_2"
    assert users[1].name == "another_user"
    assert users[1].password == repo.hash_password("another_password")
    assert users[1].date_joined == "2024-01-01T12:00:00"

def test_load_from_empty_database(mock_firebase_admin):
    _, mock_ref = mock_firebase_admin
    mock_ref.get.return_value = {} # Simulate an empty Firebase response
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    users = repo.load_from_database()
    
    # Ensure no users are loaded
    assert len(users) == 0 

def test_check_if_username_exists(mock_firebase_admin):
    _, _ = mock_firebase_admin
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    repo.load_from_database()  # Load mocked users
    
    # Test for existing username
    assert repo.check_if_username_exists("test_user") is True
    
    # Test for non-existing username
    assert repo.check_if_username_exists("non_existing_user") is False

def test_get_next_user_id(mock_firebase_admin):
    _, _ = mock_firebase_admin

    # Initialize repository with mock data
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    repo.load_from_database()

    # Add mock users
    repo.users.append(User(id="user_3", name="user3", password="abcdefghijkl", date_joined="2023-01-01T12:00:00"))
    repo.users.append(User(id="user_10", name="user10", password="abcdefghijkl", date_joined="2023-01-01T12:00:00"))

    # Test the next user ID generation
    next_id = repo.get_next_user_id()
    assert next_id == "user_11"

def test_create_user(mock_firebase_admin):
    _, _ = mock_firebase_admin
    
    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    
    # Create a user
    user_id = "user_123"
    username = "some_user"
    password = "random_password"
    user = repo.create_user(user_id, username, password)
    
    # Verify the user object
    assert isinstance(user, User)
    assert user.id == user_id
    assert user.name == username.strip()
    assert user.password == hashlib.sha256(password.strip().encode()).hexdigest()
    assert datetime.fromisoformat(user.date_joined)  # Ensure date is valid ISO format

def test_save_to_repo(mock_firebase_admin):
    _, _ = mock_firebase_admin

    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    
    # Create a user and save to repo
    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_repo(user)
    
    # Verify the user is added to the repo's users list
    assert len(repo.users) == 1
    assert repo.users[0] == user

def test_save_to_repo_invalid_user(mock_firebase_admin):
    _, _ = mock_firebase_admin

    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    
    # Attempt to save an invalid user
    with pytest.raises(ValueError, match="Invalid user object"):
        repo.save_to_repo("not_a_user_object")

def test_save_to_database(mock_firebase_admin):
    _, mock_ref = mock_firebase_admin

    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    
    # Create a user and save to database
    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_database(user)
    
    # Verify the Firebase database set call
    mock_ref.child.assert_called_once_with("user_123")
    mock_ref.child().set.assert_called_once_with({
        "username": "some_user",
        "password": "random_password",
        "date_joined": "2023-01-01T12:00:00"
    })

def test_hash_password(mock_firebase_admin):
    _, _ = mock_firebase_admin

    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    
    # Hash a password
    password = "secure_password"
    hashed = repo.hash_password(password)
    
    # Verify the hash
    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    assert hashed == expected_hash
