import pytest
from app.models import Role, User
from app.extensions import db
from app.utils.auth import generate_jwt


@pytest.fixture
def user():
    """Fixture to create a regular user."""
    user = User(
        username="testuser", email="testuser@example.com", password="hashedpassword"
    )
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def admin_user():
    """Fixture to create an admin user."""
    user = User(
        username="admin",
        email="admin@example.com",
        password="hashedpassword",
        is_active=True,
    )
    db.session.add(user)
    db.session.commit()
    return user


def test_create_role(client):
    """Test creating a new role successfully."""
    role_data = {"role_name": "Manager", "department_name": "Sales"}
    response = client.post("/roles", json=role_data)

    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Role created successfully"
    assert "role_id" in json_data


def test_create_duplicate_role(client):
    """Test creating a duplicate role in the same department."""
    role_data = {"role_name": "Manager", "department_name": "Sales"}
    client.post("/roles", json=role_data)

    response = client.post("/roles", json=role_data)
    print("================", response)
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "Role already exists in this department"


def test_create_role_case_insensitivity(client):
    """Test role creation is case insensitive."""
    role_data_1 = {"role_name": "manager", "department_name": "Sales"}
    role_data_2 = {"role_name": "Manager", "department_name": "Sales"}

    client.post("/roles", json=role_data_1)
    response = client.post("/roles", json=role_data_2)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "Role already exists in this department"


def test_assign_role_to_user(client, user):
    """Test assigning a role to a user."""

    role_data = {"role_name": "Manager", "department_name": "Sales"}
    role_response = client.post("/roles", json=role_data)
    role_id = role_response.get_json()["role_id"]

    assign_data = {"user_id": user.id, "role_id": role_id}
    response = client.post("/roles/assign", json=assign_data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == f"Role 'Manager' assigned to user '{user.username}'"


def test_assign_role_to_nonexistent_user(client):
    """Test assigning a role to a non-existent user."""

    role_data = {"role_name": "Developer", "department_name": "Engineering"}
    role_response = client.post("/roles", json=role_data)
    role_id = role_response.get_json()["role_id"]

    assign_data = {
        "user_id": 9999,
        "role_id": role_id,
    }  # Assuming user ID 9999 does not exist
    response = client.post("/roles/assign", json=assign_data)

    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "User not found"


def test_assign_nonexistent_role_to_user(client, user):
    """Test assigning a non-existent role to a user."""
    assign_data = {
        "user_id": user.id,
        "role_id": 9999,
    }  # Assuming role ID 9999 does not exist
    response = client.post("/roles/assign", json=assign_data)

    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Role not found"


def test_assign_role_to_user_twice(client, user):
    """Test assigning the same role to a user twice."""
    role_data = {"role_name": "Analyst", "department_name": "Finance"}
    role_response = client.post("/roles", json=role_data)
    role_id = role_response.get_json()["role_id"]

    assign_data = {"user_id": user.id, "role_id": role_id}
    client.post("/roles/assign", json=assign_data)

    response = client.post("/roles/assign", json=assign_data)

    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "User already has this role"


def test_assign_super_role_activates_user(client, user):
    """Test assigning the 'super' role automatically activates the user."""
    role_data = {"role_name": "super", "department_name": "Admin"}
    role_response = client.post("/roles", json=role_data)
    role_id = role_response.get_json()["role_id"]

    assign_data = {"user_id": user.id, "role_id": role_id}
    response = client.post("/roles/assign", json=assign_data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["message"] == f"Role 'Super' assigned to user '{user.username}'"

    user = db.session.get(User, user.id)
    assert user.is_active
