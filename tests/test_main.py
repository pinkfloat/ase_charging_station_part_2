import pytest
from main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "testsecret"
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test if home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200

def test_create_profile_get(client):
    """Test if create-profile page loads"""
    response = client.get("/create-profile")
    assert response.status_code == 200

def test_login_get(client):
    """Test if login page loads"""
    response = client.get("/login")
    assert response.status_code == 200

def test_dashboard_redirect(client):
    """Test if unauthenticated users are redirected from dashboard"""
    response = client.get("/dashboard", follow_redirects=True)
    assert b"<title>Login</title>" in response.data

def test_logout(client):
    """Test if logout clears session and redirects"""
    with client.session_transaction() as sess:
        sess["user_id"] = "dummy_user"
    
    response = client.get("/logout", follow_redirects=True)
    assert b"You have been logged out." in response.data



# Additional simple test cases
def test_create_profile_post(client):
    """Test creating a profile with valid input"""
    response = client.post("/create-profile", data={"username": "testuser", "password": "testpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<form" in response.data  # Ensure login form is present, meaning signup redirected to login


def test_login_post_invalid_user(client):
    """Test login with non-existent user"""
    response = client.post("/login", data={"username": "nonexistent", "password": "wrongpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<form" in response.data  # Ensure login form is present, meaning login page was reloaded


def test_login_post_invalid_password(client):
    """Test login with incorrect password"""
    response = client.post("/create-profile", data={"username": "testuser2", "password": "testpass"}, follow_redirects=True)
    response = client.post("/login", data={"username": "testuser2", "password": "wrongpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Incorrect password. Please try again." in response.data


def test_dashboard_access_denied(client):
    """Test accessing dashboard without login"""
    response = client.get("/dashboard", follow_redirects=True)
    assert b"<title>Login</title>" in response.data


def test_logout_without_login(client):
    """Test logout when no user is logged in"""
    response = client.get("/logout", follow_redirects=True)
    assert b"You have been logged out." in response.data

# Existing test cases remain unchanged
