# user/tests/infrastructure/repositories/test_user_repository.py
import pytest
from unittest.mock import MagicMock
import hashlib
from datetime import datetime
from user.src.infrastructure.repositories.user_repository import UserRepository
from user.src.domain.events.user_created_event import UserCreatedEvent
from user.src.domain.entities.user import User

import firebase_admin
from firebase_admin import credentials


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

def test_load_from_database(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
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
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")
    users = repo.load_from_database()

    assert len(users) == 0

def test_check_if_username_exists(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")
    repo.load_from_database()

    assert repo.check_if_username_exists("test_user") is True
    assert repo.check_if_username_exists("non_existing_user") is False

def test_get_next_user_id(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")
    repo.load_from_database()
    repo.users.append(User(id="user_3", name="user3", password="pass", date_joined="2023-01-01T12:00:00"))
    repo.users.append(User(id="user_10", name="user10", password="pass", date_joined="2023-01-01T12:00:00"))

    next_id = repo.get_next_user_id()
    assert next_id == "user_11"

@pytest.fixture
def mock_event_publisher():
    return MagicMock()

def test_create_user_with_event(mock_event_publisher, mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path", event_publisher=mock_event_publisher)

    user_id = "user_123"
    username = "some_user"
    password = "random_password"

    user = repo.create_user(user_id, username, password)

    assert isinstance(user, User)
    assert user.id == user_id
    assert user.name == username.strip()
    assert user.password == hashlib.sha256(password.strip().encode()).hexdigest()
    assert datetime.fromisoformat(user.date_joined)

    mock_event_publisher.assert_called_once()

    event = mock_event_publisher.call_args[0][0]
    assert isinstance(event, UserCreatedEvent)
    assert event.user == user

def test_save_to_repo(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")

    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_repo(user)

    assert len(repo.users) == 1
    assert repo.users[0] == user

def test_save_to_repo_invalid_user(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")

    with pytest.raises(ValueError, match="Invalid user object"):
        repo.save_to_repo("not_a_user_object")

def test_save_to_database(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")

    user = User("user_123", "some_user", "random_password", "2023-01-01T12:00:00")
    repo.save_to_database(user)

    saved_user = mock_database.data["user_123"]
    assert saved_user["username"] == "some_user"
    assert saved_user["password"] == "random_password"
    assert saved_user["date_joined"] == "2023-01-01T12:00:00"

def test_save_invalid_user_to_database(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")

    invalid_user = {"id": "user_123", "name": "some_user"}  # Passing a dictionary instead of a User object
    
    with pytest.raises(ValueError, match="Invalid user object"):
        repo.save_to_database(invalid_user)

def test_hash_password(mock_database, monkeypatch):
    """Fixture to create a mock repository with monkeypatched Firebase app."""
    # Prevent Firebase from initializing by faking existing apps
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])
    repo = UserRepository("mocked_path")

    password = "secure_password"
    hashed = repo.hash_password(password)

    expected_hash = hashlib.sha256(password.encode()).hexdigest()
    assert hashed == expected_hash





## new additional test cases



def test_firebase_initialization_when_not_initialized(monkeypatch):
    """
    Test that when no Firebase app is initialized (firebase_admin._apps is empty),
    the repository initializes Firebase using the provided certificate and settings.
    """
    monkeypatch.setattr(firebase_admin, '_apps', [])

    fake_cert = MagicMock(name="FakeCertificate")
    fake_initialize_app = MagicMock(name="initialize_app")

    monkeypatch.setattr(credentials, 'Certificate', lambda path: fake_cert)
    monkeypatch.setattr(
        "user.src.infrastructure.repositories.user_repository.initialize_app",
        fake_initialize_app
    )
    monkeypatch.setattr(firebase_admin, 'get_app', lambda name="[DEFAULT]": MagicMock())

    firebase_secret_json = "path/to/fake/firebase_secret.json"
    _ = UserRepository(firebase_secret_json)

    fake_initialize_app.assert_called_once_with(
        fake_cert,
        {'databaseURL': 'https://ase-charging-default-rtdb.europe-west1.firebasedatabase.app/'}
    )






def test_firebase_initialization_skipped_when_already_initialized(monkeypatch):
    """
    Test that Firebase initialization is skipped when an app is already initialized.
    """
    # Simulate an initialized Firebase app
    monkeypatch.setattr(firebase_admin, '_apps', ['dummy_app'])

    # Mock initialize_app to verify it is NOT called
    fake_initialize_app = MagicMock(name="initialize_app")
    monkeypatch.setattr(
        "user.src.infrastructure.repositories.user_repository.initialize_app",
        fake_initialize_app
    )

    # Mock get_app to return a dummy app to prevent ValueError
    monkeypatch.setattr(firebase_admin, 'get_app', lambda name="[DEFAULT]": MagicMock())

    # Trigger the UserRepository initialization
    _ = UserRepository("mocked_path")

    # Assert that initialize_app was NOT called since an app already exists
    fake_initialize_app.assert_not_called()




def test_firebase_initialization_failure(monkeypatch):
    """
    Test that an exception is raised if Firebase initialization fails.
    """
    monkeypatch.setattr(firebase_admin, '_apps', [])

    fake_cert = MagicMock(name="FakeCertificate")

    # Simulate an exception during initialization
    def fake_initialize_app_failure(*args, **kwargs):
        raise RuntimeError("Firebase initialization failed!")

    monkeypatch.setattr(credentials, 'Certificate', lambda path: fake_cert)
    monkeypatch.setattr(
        "user.src.infrastructure.repositories.user_repository.initialize_app",
        fake_initialize_app_failure
    )

    with pytest.raises(RuntimeError, match="Firebase initialization failed!"):
        _ = UserRepository("path/to/fake/firebase_secret.json")

def test_firebase_initialization_invalid_certificate(monkeypatch):
    """
    Test behavior when an invalid Firebase certificate path causes an error.
    """
    monkeypatch.setattr(firebase_admin, '_apps', [])

    # Simulate an error when trying to load an invalid certificate
    def fake_certificate_failure(path):
        raise FileNotFoundError("Invalid Firebase certificate path!")

    fake_initialize_app = MagicMock(name="initialize_app")
    monkeypatch.setattr(credentials, 'Certificate', fake_certificate_failure)
    monkeypatch.setattr(
        "user.src.infrastructure.repositories.user_repository.initialize_app",
        fake_initialize_app
    )

    with pytest.raises(FileNotFoundError, match="Invalid Firebase certificate path!"):
        _ = UserRepository("invalid/path/to/firebase_secret.json")
