# tests/application/services/test_user_service.py
import pytest
import hashlib
from unittest.mock import patch, MagicMock
from infrastructure.repositories.user_repository import UserRepository
from application.services.user_service import UserService

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

def test_create_user(mock_firebase_admin):
    _, mock_ref = mock_firebase_admin

    # Initialize repository with mock data
    repo = UserRepository("mocked/path/to/secret/firebase.json")
    repo.load_from_database()

    # Initialize service
    service = UserService(repo)

    # Create a new user
    new_user = service.create_user("another_another_user", "very_secure_password")

    # Verify the new user was created correctly
    assert new_user.id == "user_3"
    assert new_user.name == "another_another_user"
    assert new_user.password == repo.hash_password("very_secure_password")

    # Verify that the user was saved to the UserRepository
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

    # Initialize service
    service = UserService(repo)

    # Test empty username
    with pytest.raises(ValueError, match="Username cannot be empty."):
        service.create_user("", "secure_password")

    # Test empty password
    with pytest.raises(ValueError, match="Password cannot be empty."):
        service.create_user("new_user", "")

    # Test duplicate username
    with pytest.raises(ValueError, match="Username already exists. Please choose another."):
        service.create_user("test_user", "some_password")
