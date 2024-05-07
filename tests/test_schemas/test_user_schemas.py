import uuid
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, LoginRequest

# Define fixtures for reusable data structures
@pytest.fixture
def base_user_data():
    return {
        "email": "john.doe@example.com",
        "nickname": "john_doe_123",
        "first_name": "John",
        "last_name": "Doe",
        "bio": "I am a software engineer with over 5 years of experience.",
        "profile_picture_url": "https://example.com/profile.jpg",
        "linkedin_profile_url": "https://linkedin.com/in/johndoe",
        "github_profile_url": "https://github.com/johndoe",
        "role": "ADMIN"  # Assuming your UserRole enum can be directly used as a string
    }

@pytest.fixture
def create_user_data(base_user_data):
    return {**base_user_data, "password": "SecurePassword123!"}

@pytest.fixture
def update_user_data():
    return {
        "email": "new.john.doe@example.com",
        "nickname": "new_john_doe",
        "first_name": "NewJohn",
        "last_name": "NewDoe",
        "bio": "Updated bio for John."
    }

@pytest.fixture
def user_response_data(base_user_data):
    return {
        "id": uuid.uuid4(),
        **base_user_data,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "last_login_at": datetime.utcnow(),
        "links": [{"rel": "self", "href": "https://example.com/users/123"}]
    }

# Fixture for login data
@pytest.fixture
def login_request_data():
    return {
        "email": "john.doe@example.com",
        "password": "SecurePassword123!"
    }

# Define tests
def test_user_base_valid(base_user_data):
    user = UserBase(**base_user_data)
    assert user.email == base_user_data["email"]

def test_user_create_valid(create_user_data):
    user = UserCreate(**create_user_data)
    assert user.email == create_user_data["email"]

def test_user_update_valid(update_user_data):
    user_update = UserUpdate(**update_user_data)
    assert user_update.email == update_user_data["email"]

def test_user_response_valid(user_response_data):
    user_response = UserResponse(**user_response_data)
    assert user_response.id == user_response_data["id"]

def test_login_request_valid(login_request_data):
    login_request = LoginRequest(**login_request_data)
    assert login_request.email == login_request_data["email"]

@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, base_user_data):
    base_user_data["nickname"] = nickname
    user = UserBase(**base_user_data)
    assert user.nickname == nickname

@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, base_user_data):
    base_user_data["profile_picture_url"] = url
    user = UserBase(**base_user_data)
    assert user.profile_picture_url == url
