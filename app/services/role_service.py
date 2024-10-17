from app.models import Role, User
from app.extensions import db
from sqlalchemy.exc import IntegrityError


def create_role(role_name, department_name):
    """Create a new role with a unique combination of role_name and department_name."""
    try:
        existing_role = Role.query.filter_by(
            role_name=role_name, department_name=department_name
        ).first()

        if existing_role:
            return {"message": "Role already exists in this department"}, 400

        new_role = Role(role_name=role_name.lower(), department_name=department_name)
        db.session.add(new_role)
        db.session.commit()

        return {
            "message": "Role created successfully",
            "role_id": new_role.role_id,
        }, 201

    except IntegrityError:
        db.session.rollback()
        return {"message": "Role already exists in this department"}, 400


def assign_role_to_user(user_id, role_id):
    """Assign a role to a user by their IDs."""
    user = db.session.get(User, int(user_id))
    role = db.session.get(Role, int(role_id))

    if not user:
        return {"message": "User not found"}, 404
    if not role:
        return {"message": "Role not found"}, 404

    if role in user.roles:
        return {"message": "User already has this role"}, 400

    user.roles.append(role)

    if role.role_name.lower() == "super":
        user.is_active = True

    db.session.commit()
    return {
        "message": f"Role '{role.role_name.capitalize()}' assigned to user '{user.username}'"
    }, 200
