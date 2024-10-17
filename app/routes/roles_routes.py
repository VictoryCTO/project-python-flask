from flask import Blueprint, jsonify, request
from app.services.role_service import create_role, assign_role_to_user

role_bp = Blueprint("role_bp", __name__)


@role_bp.route("/roles", methods=["POST"])
def create_userrole():
    """Create a new role."""
    data = request.get_json()
    role_name = data.get("role_name")
    department_name = data.get("department_name")

    result, status_code = create_role(role_name, department_name)

    return jsonify(result), status_code


@role_bp.route("/roles/assign", methods=["POST"])
def assign_userrole():
    """Assign a role to a user."""
    data = request.get_json()
    user_id = data.get("user_id")
    role_id = data.get("role_id")

    result, status_code = assign_role_to_user(user_id, role_id)

    return jsonify(result), status_code
