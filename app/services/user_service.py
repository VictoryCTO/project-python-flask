from datetime import datetime, timezone
from ..models import User
from ..extensions import db, bcrypt


def create_user(username, email, password):
    required_fields = {"username": username, "email": email, "password": password}

    for field_name, value in required_fields.items():
        if not value:
            return {"message": f"{field_name.capitalize()} is required"}, 400

    existing_user = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()
    if existing_user:
        return {"message": "Username or email already exists"}, 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    new_user = User(
        username=username, email=email, password=hashed_password, is_active=False
    )
    db.session.add(new_user)
    db.session.commit()
    return {"message": "User registered successfully", "email": new_user.email}


def check_password(email, password):
    user = User.query.filter_by(email=email).first()

    if not user:
        print("user not found")
        return False

    if bcrypt.check_password_hash(user.password, password):
        return True
    else:
        return False


def toggle_user_status(identifier, activate):
    if isinstance(identifier, int):
        user = db.session.get(
            User, identifier
        )  # Use Session.get() instead of Query.get()
    else:
        return {"message": "Invalid identifier type"}, 400

    if not user:
        return {"message": "User not found"}, 404

    user.is_active = activate
    user.inactivated_on = (
        None if activate else datetime.now(timezone.utc)
    )  # Use timezone-aware datetime

    db.session.commit()

    status = "activated" if activate else "deactivated"
    return {"message": f"User {user.username} has been {status}"}, 200


def make_user_admin(user_id=None):
    if user_id:
        user = User.query.get(user_id)

    if not user:
        return {"message": "User not found"}, 404

    user.role = "admin"
    db.session.commit()
    return {"message": f"User {user.username} has been made an admin."}, 200
