import pytest
from app.models import User, Role
from app.extensions import db
from app.utils.auth import generate_jwt


@pytest.fixture
def admin_user():
    """Fixture to create an admin user with the 'admin' role."""
    user = User(
        username="admin",
        email="admin@example.com",
        password="hashedpassword",
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()

    admin_role = Role.query.filter_by(role_name="admin").first()
    if not admin_role:
        admin_role = Role(role_name="admin", department_name="general")
        db.session.add(admin_role)
        db.session.commit()

    user.roles.append(admin_role)
    db.session.commit()
    return user


@pytest.fixture
def regular_user():
    """Fixture to create a regular (non-admin) user."""
    user = User(
        username="testuser",
        email="testuser@example.com",
        password="hashedpassword",
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_register_user(client):
    # Prepare the test data
    data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }

    # Send a POST request to register a new user
    response = client.post("/register", json=data)

    # Assert that the response status code is 201 (Created)
    assert response.status_code == 201

    # Assert that the response JSON contains the expected message
    json_data = response.get_json()
    assert json_data["message"] == "User registered successfully"
    assert json_data["email"] == "testuser@example.com"


def test_register_user_with_existing_email(client):
    data = {
        "username": "testuser",
        "email": "duplicate@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=data)

    response = client.post("/register", json=data)
    assert response.status_code == 400
    json_data = response.get_json()

    assert json_data[0]["message"] == "Username or email already exists"


@pytest.mark.parametrize(
    "missing_field, data",
    [
        ("username", {"email": "testuser2@example.com", "password": "testpassword"}),
        ("email", {"username": "testuser", "password": "testpassword"}),
        ("password", {"username": "testuser", "email": "testuser2@example.com"}),
    ],
)
def test_register_user_missing_fields(client, missing_field, data):
    response = client.post("/register", json=data)

    assert response.status_code == 400

    json_data = response.get_json()
    assert json_data[0]["message"] == f"{missing_field.capitalize()} is required"


def test_login_user(client):
    # First, register a new user
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    user = User.query.filter_by(email="testuser@example.com").first()
    user.is_active = True
    db.session.commit()

    # Prepare login data
    login_data = {"email": "testuser@example.com", "password": "testpassword"}

    # Send a POST request to login
    response = client.post("/login", json=login_data)

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the response JSON contains the expected message
    json_data = response.get_json()
    assert json_data["message"] == "Login successful"
    assert "token" in json_data


def test_login_invalid_password(client):
    # Prepare invalid login data
    register_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword",
    }
    client.post("/register", json=register_data)

    login_data = {"email": "testuser@example.com", "password": "wrongpassword"}

    user = User.query.filter_by(email="testuser@example.com").first()
    user.is_active = True

    # Send a POST request to login
    # use the wrong password to test the invalid login
    db.session.commit()
    response = client.post("/login", json=login_data)
    assert response.status_code == 401

    json_data = response.get_json()
    assert json_data["message"] == "Invalid credentials"


def test_login_unregistered_user(client):
    login_data = {"email": "unknown@example.com", "password": "testpassword"}

    response = client.post("/login", json=login_data)
    assert response.status_code == 401

    json_data = response.get_json()
    assert json_data["message"] == "Invalid credentials"


def test_login_missing_fields(client):
    login_data = {"email": "testuser@example.com"}

    response = client.post("/login", json=login_data)

    assert response.status_code == 400

    json_data = response.get_json()
    assert json_data["message"] == "Password is required"


def test_toggle_status_activate(client, admin_user, regular_user):
    admin_token = generate_jwt(admin_user)
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.put(
        "/toggle_user_status",
        json={"user_id": regular_user.id, "activate": False},
        headers=headers,
    )
    assert response.status_code == 200
    assert (
        response.get_json()["message"]
        == f"User {regular_user.username} has been deactivated"
    )

    user = db.session.get(User, regular_user.id)  # Use db.session.get()
    assert not user.is_active


def test_toggle_status_deactivate(client, admin_user, regular_user):
    admin_token = generate_jwt(admin_user)
    headers = {"Authorization": f"Bearer {admin_token}"}

    response = client.put(
        "/toggle_user_status",
        json={"user_id": regular_user.id, "activate": True},
        headers=headers,
    )
    assert response.status_code == 200
    assert (
        response.get_json()["message"]
        == f"User {regular_user.username} has been activated"
    )

    user = db.session.get(User, regular_user.id)
    assert user.is_active


def test_login_inactive_user(client, regular_user):
    with client.application.app_context():
        regular_user.is_active = False
        db.session.commit()

    login_data = {"email": regular_user.email, "password": "testpassword"}

    response = client.post("/login", json=login_data)

    assert response.status_code == 403

    json_data = response.get_json()
    assert json_data["message"] == "Account is inactive"
