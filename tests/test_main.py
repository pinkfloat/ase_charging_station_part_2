import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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












def test_non_existent_route(client):
    """Test accessing a non-existent route"""
    response = client.get("/some-random-page")
    assert response.status_code == 404

def test_login_page_access(client):
    """Test accessing login page without session"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data

def test_dashboard_invalid_session(client):
    """Test if dashboard redirects if session has invalid user_id"""
    with client.session_transaction() as sess:
        sess["user_id"] = "invalid_user"
    response = client.get("/dashboard", follow_redirects=True)
    assert b"<title>Login</title>" in response.data

def test_create_profile_empty_fields(client):
    """Test creating a profile with empty username/password"""
    response = client.post("/create-profile", data={"username": "", "password": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<form" in response.data




def test_non_existent_route(client):
    """Test accessing a non-existent route"""
    response = client.get("/some-random-page")
    assert response.status_code == 404

def test_login_page_access(client):
    """Test accessing login page without session"""
    response = client.get("/login")
    assert response.status_code == 200
    assert b"<form" in response.data

def test_dashboard_invalid_session(client):
    """Test if dashboard redirects if session has invalid user_id"""
    with client.session_transaction() as sess:
        sess["user_id"] = "invalid_user"
    response = client.get("/dashboard", follow_redirects=True)
    assert b"<title>Login</title>" in response.data

def test_create_profile_empty_fields(client):
    """Test creating a profile with empty username/password"""
    response = client.post("/create-profile", data={"username": "", "password": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<form" in response.data

def test_login_empty_fields(client):
    """Test login with empty username/password"""
    response = client.post("/login", data={"username": "", "password": ""}, follow_redirects=True)
    assert response.status_code == 200
    assert b"<form" in response.data

def test_dashboard_without_auth_redirects(client):
    """Test dashboard access without authentication redirects to login"""
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data

def test_logout_redirects(client):
    """Test logout redirects to login page"""
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"<title>Login</title>" in response.data




def test_dashboard_after_login(client):
    """Test accessing dashboard after a successful login"""
    client.post("/create-profile", data={"username": "userdashboard", "password": "passdashboard"}, follow_redirects=True)
    client.post("/login", data={"username": "userdashboard", "password": "passdashboard"}, follow_redirects=True)
    response = client.get("/dashboard")
    assert response.status_code == 302  # Redirect to the Dash app

def test_logout_clears_session(client):
    """Test if logout clears session data"""
    with client.session_transaction() as sess:
        sess["user_id"] = "someuser"
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data



















def test_create_duplicate_user(client):
    """Test creating a duplicate user should fail"""
    client.post("/create-profile", data={"username": "duplicateUser", "password": "testpass"}, follow_redirects=True)
    response = client.post("/create-profile", data={"username": "duplicateUser", "password": "testpass"}, follow_redirects=True)
    assert response.status_code == 200


def test_login_after_signup(client):
    """Test logging in immediately after signing up"""
    client.post("/create-profile", data={"username": "newUser", "password": "newpass"}, follow_redirects=True)
    response = client.post("/login", data={"username": "newUser", "password": "newpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"dashboard" in response.data  # User should be redirected to the dashboard


def test_dashboard_access_after_login(client):
    """Test if a user can access the dashboard after login"""
    client.post("/create-profile", data={"username": "testdashboard", "password": "testpass"}, follow_redirects=True)
    client.post("/login", data={"username": "testdashboard", "password": "testpass"}, follow_redirects=True)
    response = client.get("/dashboard", follow_redirects=True)
    assert response.status_code == 200


def test_logout_clears_session(client):
    """Test if logout properly clears session"""
    client.post("/create-profile", data={"username": "logoutUser", "password": "logoutpass"}, follow_redirects=True)
    client.post("/login", data={"username": "logoutUser", "password": "logoutpass"}, follow_redirects=True)
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # User should be redirected to login

