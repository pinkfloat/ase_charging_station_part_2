# user/tests/application/services/test_user_service.py
import pytest
from unittest.mock import MagicMock
from user.src.application.services.user_service import UserService
from user.src.domain.entities.user import User

@pytest.fixture
def mock_user_repository():
    """Fixture for mocking the UserRepository."""
    mock_repo = MagicMock()
    mock_repo.check_if_username_exists.return_value = False
    mock_repo.get_next_user_id.return_value = 1
    return mock_repo

@pytest.fixture
def user_service(mock_user_repository):
    """Fixture for creating a UserService with a mocked repository."""
    return UserService(user_repository=mock_user_repository)

def test_create_user_valid_input(user_service, mock_user_repository):
    """Test creating a user with valid input."""
    username = "testuser"
    password = "securepassword"
    
    user = user_service.create_user(username, password)

    mock_user_repository.check_if_username_exists.assert_called_once_with(username)
    mock_user_repository.get_next_user_id.assert_called_once()
    mock_user_repository.create_user.assert_called_once_with(1, username, password)
    mock_user_repository.save_to_repo.assert_called_once_with(user)
    mock_user_repository.save_to_database.assert_called_once_with(user)

def test_create_user_empty_username(user_service):
    """Test that creating a user with an empty username raises ValueError."""
    with pytest.raises(ValueError, match="Username cannot be empty."):
        user_service.create_user("", "securepassword")

def test_create_user_empty_password(user_service):
    """Test that creating a user with an empty password raises ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty."):
        user_service.create_user("testuser", "")

def test_create_user_username_already_exists(user_service, mock_user_repository):
    """Test that creating a user with a duplicate username raises ValueError."""
    mock_user_repository.check_if_username_exists.return_value = True

    with pytest.raises(ValueError, match="Username already exists. Please choose another."):
        user_service.create_user("testuser", "securepassword")

def test_create_user_whitespace_username(user_service):
    """Test that creating a user with a username that is only whitespace raises ValueError."""
    with pytest.raises(ValueError, match="Username cannot be empty."):
        user_service.create_user("   ", "securepassword")

def test_create_user_whitespace_password(user_service):
    """Test that creating a user with a password that is only whitespace raises ValueError."""
    with pytest.raises(ValueError, match="Password cannot be empty."):
        user_service.create_user("testuser", "   ")

def test_get_all_users(user_service, mock_user_repository):
    """Test retrieving all users from the database."""
    mock_users = [
        User(id="user_1", name="Alice", password="hashed_pw1", date_joined="2024-01-01T12:00:00"),
        User(id="user_2", name="Bob", password="hashed_pw2", date_joined="2024-01-02T12:00:00")
    ]
    mock_user_repository.load_from_database.return_value = mock_users

    users = user_service.get_all_users()

    assert len(users) == 2
    assert users[0].name == "Alice"
    assert users[1].name == "Bob"
    mock_user_repository.load_from_database.assert_called_once()

def test_get_all_users_empty(user_service, mock_user_repository):
    """Test retrieving users when the database is empty."""
    mock_user_repository.load_from_database.return_value = []

    users = user_service.get_all_users()

    assert users == []  # Should return an empty list
    mock_user_repository.load_from_database.assert_called_once()
