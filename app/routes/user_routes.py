from flask import Blueprint, Response, jsonify, request
from ..models import User, UserActiveStatusChange
from ..extensions import db
from ..services.user_service import create_user, check_password
import logging
import sys
import json

# Configure logger to print to shell.
logger = logging.getLogger("alembic.env")
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

user_bp = Blueprint("user_bp", __name__)


# Route to register a new user.
@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    # status = defaults to inactive
    user = create_user(username, email, password)
    return jsonify({f"message": "User " + username + " registered successfully"}), 201


# Route to log in a user.
@user_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if check_password(email, password) is True:
        return jsonify({"message": "Login successful", "email": email}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Dummy profile route for the user.
@user_bp.route("/profile", methods=["GET"])
def profile():
    # In a real system, you would have authentication and user session handling
    return jsonify({"message": "User profile information"}), 200


# Route to hit to toggle active/inactive status of a user.
@user_bp.route("/toggle-active", methods=["POST"])
def toggle_active():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    else:
        user.active = not user.active
        # Save the status change to UserActiveStatusChange table.
        status_change = UserActiveStatusChange(
            id_user=user.id, status="active" if user.active else "inactive"
        )
        db.session.commit()
        return jsonify({"message": f"User status toggled to {user.active}"}), 200


# Route to show all users.
#    Deprecated in favor of access-report route.
@user_bp.route("/users", methods=["GET"])
def users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(
            {
                "user": user.username,
                "email": user.email,
                "role": user.access_level,
                "active": user.active,
            }
        )
        logger.debug(
            f"{user.username} | {user.email} | Active: {user.active} | Role: {user.access_level}"
        )
    response = json.dumps(user_list)
    return Response(response, mimetype="application/json"), 200


# Route to show all users.
@user_bp.route("/access-report", methods=["POST"])
def access_report():
    data = request.get_json()
    limit_to = data.get("limit_to")
    # limit_to may be "all_users", "active_users", or "inactive_users"
    if limit_to == "all_users":
        users = User.query.all()
    elif limit_to == "active_users":
        users = User.query.filter_by(active=True).all()
    elif limit_to == "inactive_users":
        users = User.query.filter_by(active=False).all()
    else:
        users = User.query.all()
    user_list = []
    for user in users:
        user_list.append(
            {
                "user": user.username,
                "email": user.email,
                "role": user.access_level,
                "active": user.active,
            }
        )
        logger.debug(
            f"{user.username} | {user.email} | {user.access_level} | {user.active}"
        )
    response = json.dumps(user_list)
    return Response(response, mimetype="application/json"), 200


# Route to delete a user.
@user_bp.route("/delete-user", methods=["POST"])
def delete_user():
    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    else:
        # Delete references to user in UserActiveStatusChange table.
        status_changes = UserActiveStatusChange.query.filter_by(id_user=user.id).all()
        for status_change in status_changes:
            db.session.delete(status_change)
        # Now delete the user.
        db.session.delete(user)
        db.session.commit()
        logger.debug(f"{user} deleted")
        return jsonify({"message": "User deleted"}), 200
