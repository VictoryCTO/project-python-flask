from flask import Blueprint, Response, jsonify, request
from ..models import User, UserActiveStatusChange, RolesLookup, UsersRoles
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
    # Add user authentication & session handling
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    # status = defaults to inactive
    # check to see if user already exists
    user = User.query.filter_by(email=email).first()
    if user is not None:
        return jsonify({"message": "User email already exists"}), 409
    user = User.query.filter_by(username=username).first()
    if user is not None:
        return jsonify({"message": "Username already exists"}), 409
    user = create_user(username, email, password)
    logger.debug(f"{user.username} with {user.email} created.")
    return jsonify({f"message": "User " + username + " registered successfully"}), 201


# Route to log in a user.
@user_bp.route("/login", methods=["POST"])
def login():
    # Add user authentication & session handling
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    if check_password(email, password) is True:
        return jsonify({"message": "Login successful", "email": email}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


# Profile route for the user.
@user_bp.route("/profile", methods=["POST"])
def profile():
    # Add user authentication & session handling
    data = request.get_json()
    email = data.get("email")
    username = data.get("username")
    """ If email is not provided, use username to get user_id.
    If username is not provided, use email.
    If neither, return 400."""
    if (email is None or email == "") and (username is None or username == ""):
        return jsonify({"message": "Email or username required"}), 400
    elif email is None or email == "":
        user = User.query.filter_by(username=username).first()  # Get user_id
    else:
        user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "User not found"}), 404
    else:
        # Get user profile information

        # Get the roles and departments using the users_roles table
        roles_depts = (
            db.session.query(RolesLookup.role_name, RolesLookup.department_name)
            .join(UsersRoles, RolesLookup.id == UsersRoles.role_id)
            .filter(UsersRoles.user_id == user.id)
            .all()
        )
        roles_list = []
        for role_dept in roles_depts:
            roles_list.append(f"{role_dept[0]}/{role_dept[1]}")

        # Build the user profile string
        profile = (
            f"Username: {user.username}\n"
            f"email: {user.email}\n"
            f"active: {user.active}\n"
            f"roles: {str(roles_list)}\n"
        )
        logger.debug(profile)

        return jsonify({"message": "User profile information" + profile}), 200


# Route to hit to toggle active/inactive status of a user.
@user_bp.route("/toggle-active", methods=["POST"])
def toggle_active():
    # Add user authentication & session handling
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
    # Add user authentication & session handling
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
    # Add user authentication & session handling
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


# Route to show all users and their roles.
@user_bp.route("/users-roles", methods=["GET"])
def users_roles():
    # Add user authentication & session handling
    users = User.query.all()
    user_list = []
    for user in users:
        id_user = user.id
        # for each user, get the roles and departments using the users_roles table
        roles_depts = (
            db.session.query(RolesLookup.role_name, RolesLookup.department_name)
            .join(UsersRoles, RolesLookup.id == UsersRoles.role_id)
            .filter(UsersRoles.user_id == id_user)
            .all()
        )
        roles_list = []
        for role_dept in roles_depts:
            roles_list.append(f"{role_dept[0]}/{role_dept[1]}")

        user_list.append(
            {
                "user": user.username,
                "email": user.email,
                "roles": str(roles_list),
                "active": user.active,
            }
        )
        logger.debug(
            f"{user.username} | {user.email} | Active: {user.active} | Roles: {str(roles_list)}"
        )
    response = json.dumps(user_list)
    return Response(response, mimetype="application/json"), 200


# Route to delete a user.
@user_bp.route("/delete-user", methods=["POST"])
def delete_user():
    # Add user authentication & session handling
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


""" Create role(s)/dept(s) in roles_lookup with attributes role_name and department_name.
Combination of role_name and department_name is unique. """


@user_bp.route("/create-roles", methods=["POST"])
def create_roles():
    # Add user authentication & session handling
    """POST looks like:
    Invoke-WebRequest -Uri http://127.0.0.1:5000/create-roles -Method POST -Headers @{"Content-Type" = "application/json"}
    -Body '{"role_dept":"dev,accounting", "role_dept":"admin,logistics"}'"""
    data = request.get_json()
    # The following line is only getting the first role_dept, not all of them.
    roles_depts = data.get("roles_depts")  # Expecting a list of roles and departments
    logger.debug(f"roles_depts={str(roles_depts)}")
    # Add input validation here.
    # Add error checking.
    for role_dept in roles_depts:
        # logger.debug(f"role_dept={str(role_dept)}")
        # Chose not to use tuple unpacking below, for clarity/debugging/scalability.
        role_name = role_dept.split(",")[0]
        dept_name = role_dept.split(",")[1]

        # Check if the role/dept combos exist and if not, add to roles_lookup
        role_exists = RolesLookup.query.filter_by(
            role_name=role_name, department_name=dept_name
        ).first()
        if role_exists is None:
            logger.debug(f"Role/dept {role_name}/{dept_name} combination not found")
            new_role = RolesLookup(role_name=role_name, department_name=dept_name)
            logger.debug(f"Role/dept {role_name}/{dept_name} combination added")
            db.session.add(new_role)
            db.session.commit()

    return jsonify({"message": "Roles created"}), 201


""" Allow for a user to be assigned one or more roles.
    This will be done by adding record(s) to the users_roles table.
    Potential for this to receive a list of roles to assign to a user
    or a list of users (via email) to assign role(s) to. """


@user_bp.route("/assign-roles", methods=["POST"])
def assign_roles():
    """POST looks like:
    Invoke-WebRequest -Uri http://127.0.0.1:5000/assign-roles -Method POST -Headers @{"Content-Type" = "application/json"}
    -Body '{"emails_roles_depts":["bozo@oceanmedia.net,dev,accounting", "scotter@oceanmedia.net,admin,logistics"]}'
    """

    data = request.get_json()
    emails_roles_depts = data.get(
        "emails_roles_depts"
    )  # Expecting a list of roles and departments

    if not emails_roles_depts:
        return jsonify({"message": "Invalid input"}), 400

    for email_role_dept in emails_roles_depts:
        parts = email_role_dept.split(",")
        if len(parts) != 3:
            logger.debug(f"Invalid entry: {email_role_dept}")
            continue

        user_email, role_name, dept_name = parts

        # Check if the role/dept combo exists and if not, add to roles_lookup
        role_exists = RolesLookup.query.filter_by(
            role_name=role_name, department_name=dept_name
        ).first()
        if role_exists is None:
            new_role = RolesLookup(role_name=role_name, department_name=dept_name)
            db.session.add(new_role)
            db.session.commit()
            role_exists = new_role

        # Assign the role to the user
        user = User.query.filter_by(email=user_email).first()
        if user is None:
            logger.debug(f"User with email {user_email} not found.")
            continue

        user_role_exists = UsersRoles.query.filter_by(
            user_id=user.id, role_id=role_exists.id
        ).first()
        if user_role_exists is None:
            user_role = UsersRoles(user_id=user.id, role_id=role_exists.id)
            db.session.add(user_role)

    db.session.commit()
    logger.debug(f"Role(s) assigned.")
    return jsonify({"message": "Roles assigned"}), 200
