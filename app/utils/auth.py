import jwt
from flask import request, jsonify
from functools import wraps
from datetime import datetime, timedelta, timezone
from ..models import User
from ..extensions import db

from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def generate_jwt(user):
    """Generate a JWT token for a user."""
    payload = {
        "user_id": user.id,
        "role": user.role,
        "exp": datetime.now(timezone.utc) + timedelta(hours=1),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


def decode_jwt(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def admin_required(f):
    """Decorator to check if the user has an admin role."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        token = token.split(" ")[1]  # Assume token is in the format "Bearer <token>"
        payload = decode_jwt(token)

        if not payload or payload.get("role") != "admin":
            return jsonify({"message": "Admin access required"}), 403

        return f(*args, **kwargs)

    return decorated_function
