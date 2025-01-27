# tests/infrastructure/repositories/test_user_repository.py
import pytest
import hashlib
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
    _, mock_ref = mock_firebase_admin

    # Initialize repository with mock data
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    repo.load_from_database()

    # Create a new user
    new_user = repo.create_user("another_another_user", "very_secure_password")

    # Verify the new user was created correctly
    assert new_user.id == "user_3"
    assert new_user.name == "another_another_user"
    assert new_user.password == repo.hash_password("very_secure_password")
    assert new_user in repo.users

    # Verify that the user was saved to Firebase
    mock_ref.child.assert_called_with(new_user.id)
    mock_ref.child(new_user.id).set.assert_called_with({
        "username": "another_another_user",
        "password": repo.hash_password("very_secure_password"),
        "date_joined": new_user.date_joined
    })

def test_create_user_validation(mock_firebase_admin):
    _, _ = mock_firebase_admin

    # Initialize repository
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    repo.load_from_database()

    # Test empty username
    with pytest.raises(ValueError, match="Username cannot be empty."):
        repo.create_user("", "secure_password")

    # Test empty password
    with pytest.raises(ValueError, match="Password cannot be empty."):
        repo.create_user("new_user", "")

    # Test duplicate username
    with pytest.raises(ValueError, match="Username already exists. Please choose another."):
        repo.create_user("test_user", "some_password")
