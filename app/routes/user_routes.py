from flask import Blueprint, jsonify, request
from ..models import User
from ..extensions import db
from ..services.user_service import (
    create_user,
    check_password,
    toggle_user_status,
    make_user_admin,
)
from ..utils.auth import generate_jwt, admin_required

user_bp = Blueprint("user_bp", __name__)


@user_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    result = create_user(username, email, password)

    if "message" in result and result["message"] == "User registered successfully":
        return jsonify(result), 201
    else:
        return jsonify(result), 400


@user_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email:
            return jsonify({"message": "Email is required"}), 400
        if not password:
            return jsonify({"message": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()

        if user and user.is_active and check_password(email, password):
            token = generate_jwt(user)
            return jsonify({"message": "Login successful", "token": token}), 200
        elif user and not user.is_active:
            return jsonify({"message": "Account is inactive"}), 403
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"message": "An unexpected error occurred"}), 500


@user_bp.route("/profile", methods=["GET"])
def profile():
    # Dummy profile route for the user
    # In a real system, you would have authentication and user session handling
    return jsonify({"message": "User profile information"}), 200


@user_bp.route("/toggle_user_status", methods=["PUT"])
@admin_required
def toggle_status():
    data = request.get_json()
    activate = data.get("activate", False)
    user_id = data.get("user_id")

    if user_id:
        user_id = int(user_id)
    else:
        return jsonify({"message": "Please provide 'user_id'"}), 400

    result, status_code = toggle_user_status(user_id, activate)
    return jsonify(result), status_code


@user_bp.route("/make_admin", methods=["PUT"])
def make_admin():
    data = request.get_json()
    user_id = data.get("user_id")

    result, status_code = make_user_admin(user_id=user_id)
    return jsonify(result), status_code
